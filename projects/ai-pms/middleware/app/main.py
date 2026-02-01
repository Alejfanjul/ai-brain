"""
AI-PMS Middleware
FastAPI application that syncs QloApps <-> Channex

Endpoints:
- POST /webhook/channex  - Receives webhooks from Channex (OTA bookings)
- POST /webhook/qloapps  - Receives webhooks from QloApps module (direct bookings)
- GET  /health           - Health check
"""
import asyncio
import json
import logging
import traceback
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional

from .config import settings, ROOM_TYPE_MAPPING, ROOM_TYPE_MAPPING_REVERSE, RATE_PLAN_MAPPING, DEFAULT_RESTRICTIONS
from .channex_client import channex
from .qloapps_client import qloapps
from .booking_store import booking_store

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Cosmo Middleware",
    description="""
Middleware que conecta o PMS (QloApps) com o Channel Manager (Channex).

**O que faz:**
- Recebe avisos de reservas novas/canceladas do QloApps e atualiza ARI (disponibilidade + tarifas) no Channex
- Recebe avisos de reservas de OTAs (Booking, Expedia) via Channex e cria no QloApps

**Como testar:**
1. Use os endpoints de "Sync Manual" abaixo pra testar a conexao com Channex
2. Os webhooks sao chamados automaticamente pelos sistemas
    """,
    version="1.0.0"
)


# === Models ===

class ChannexWebhook(BaseModel):
    event: str
    property_id: str
    timestamp: Optional[str] = None
    user_id: Optional[str] = None
    payload: Optional[dict] = None


class QloAppsWebhook(BaseModel):
    event: str
    timestamp: str
    source: str
    data: dict


# === Webhook Handlers ===

@app.post("/webhook/channex", tags=["Webhooks (automatico)"])
async def webhook_channex(webhook: ChannexWebhook, background_tasks: BackgroundTasks):
    """
    Recebe avisos do Channex (reservas de OTAs).

    Chamado automaticamente pelo Channex quando:
    - Chega reserva nova de Booking/Expedia/Airbnb
    - Reserva e modificada
    - Reserva e cancelada

    **Voce NAO precisa chamar isso manualmente.**
    """
    logger.info(f"Channex webhook received: {webhook.event}")

    if webhook.event in ("booking", "booking_new"):
        background_tasks.add_task(handle_channex_booking_new, webhook)
        return {"status": "processing", "event": webhook.event}

    elif webhook.event == "booking_modification":
        background_tasks.add_task(handle_channex_booking_modified, webhook)
        return {"status": "processing", "event": webhook.event}

    elif webhook.event == "booking_cancellation":
        background_tasks.add_task(handle_channex_booking_cancelled, webhook)
        return {"status": "processing", "event": webhook.event}

    elif webhook.event == "ari":
        # ARI changes from Channex - usually we don't need to act on these
        logger.info("ARI change notification from Channex (ignored)")
        return {"status": "ignored", "event": webhook.event}

    else:
        logger.warning(f"Unknown Channex event: {webhook.event}")
        return {"status": "ignored", "event": webhook.event}


@app.post("/webhook/qloapps", tags=["Webhooks (automatico)"])
async def webhook_qloapps(webhook: QloAppsWebhook, background_tasks: BackgroundTasks):
    """
    Recebe avisos do QloApps (reservas diretas).

    Chamado automaticamente pelo QloApps quando:
    - Reserva nova e criada no PMS
    - Reserva e atualizada
    - Reserva e cancelada

    Quando recebe, atualiza a disponibilidade no Channex automaticamente.

    **Voce NAO precisa chamar isso manualmente.**
    """
    logger.info(f"QloApps webhook received: {webhook.event}")

    if webhook.event == "booking.created":
        background_tasks.add_task(handle_qloapps_booking_created, webhook)
        return {"status": "processing", "event": webhook.event}

    elif webhook.event == "booking.updated":
        background_tasks.add_task(handle_qloapps_booking_updated, webhook)
        return {"status": "processing", "event": webhook.event}

    elif webhook.event == "booking.cancelled":
        background_tasks.add_task(handle_qloapps_booking_cancelled, webhook)
        return {"status": "processing", "event": webhook.event}

    else:
        logger.warning(f"Unknown QloApps event: {webhook.event}")
        return {"status": "ignored", "event": webhook.event}


# === Background Tasks ===

async def handle_channex_booking_new(webhook: ChannexWebhook):
    """Process new booking from Channex -> create in QloApps"""
    try:
        # 0. Extract IDs from payload
        revision_id = None
        booking_id = None

        if webhook.payload:
            booking_id = webhook.payload.get("booking_id")
            revision_id = webhook.payload.get("revision_id")

        if not booking_id and not revision_id:
            logger.error("No booking_id or revision_id in Channex webhook payload")
            return

        # 1. Idempotency check
        if booking_id and booking_store.exists(booking_id):
            existing = booking_store.get_by_channex_id(booking_id)
            logger.warning(f"Booking {booking_id} already processed -> QloApps order {existing['qloapps_order_id']}. Skipping.")
            # Still ack to stop Channex from resending
            if revision_id:
                await channex.ack_booking_revision(revision_id)
            return

        # 2. Fetch full booking details from Channex
        if revision_id:
            logger.info(f"Fetching booking revision {revision_id} from Channex...")
            response = await channex.get_booking_revision(revision_id)
        else:
            logger.info(f"Fetching booking {booking_id} from Channex...")
            response = await channex.get_booking(booking_id)

        booking = response.get("data", {}).get("attributes", {})
        booking_id = booking_id or booking.get("booking_id")
        logger.info(f"Booking details: status={booking.get('status')}, ota={booking.get('ota_name')}, unique_id={booking.get('unique_id')}")

        # 3. Transform Channex booking to QloApps format
        qloapps_booking = transform_channex_to_qloapps(booking)

        # 4. Create booking in QloApps
        logger.info("Creating booking in QloApps...")
        result = await qloapps.create_booking(qloapps_booking)
        qloapps_order_id = extract_qloapps_order_id(result)
        logger.info(f"Booking created in QloApps: order_id={qloapps_order_id}")

        # 5. Save mapping (Channex <-> QloApps)
        customer = booking.get("customer", {})
        guest_name = f"{customer.get('name', '')} {customer.get('surname', customer.get('last_name', ''))}".strip()
        booking_store.save_booking(
            channex_booking_id=booking_id,
            qloapps_order_id=qloapps_order_id,
            channex_revision_id=revision_id,
            channex_unique_id=booking.get("unique_id"),
            ota_name=booking.get("ota_name"),
            guest_name=guest_name or "Unknown",
            checkin=booking.get("arrival_date"),
            checkout=booking.get("departure_date"),
        )

        # 6. Acknowledge in Channex (AFTER create + save)
        # Only revision-level ack works (/bookings/{id}/ack returns 404)
        if revision_id:
            await channex.ack_booking_revision(revision_id)
            logger.info(f"Revision {revision_id} acknowledged in Channex")
        else:
            logger.warning(f"No revision_id to ack for booking {booking_id} — skipping ack")

        # 7. Re-sync ARI (availability decreased due to new booking)
        rooms = booking.get("rooms", [])
        if rooms:
            room = rooms[0]
            channex_room_type_id = room.get("room_type_id", "")
            qloapps_room_type_id = ROOM_TYPE_MAPPING_REVERSE.get(channex_room_type_id)
            checkin = booking.get("arrival_date")
            checkout = booking.get("departure_date")
            if qloapps_room_type_id and channex_room_type_id and checkin and checkout:
                logger.info("Re-syncing ARI after OTA booking...")
                await sync_ari_to_channex(qloapps_room_type_id, channex_room_type_id, checkin, checkout)

    except Exception as e:
        logger.error(f"Error handling Channex booking: {e}")
        logger.error(traceback.format_exc())


async def handle_channex_booking_modified(webhook: ChannexWebhook):
    """Process modified booking from Channex -> update in QloApps"""
    try:
        # Channex booking_modification webhook uses "booking_revision_id" (not "revision_id")
        revision_id = (
            webhook.payload.get("booking_revision_id")
            or webhook.payload.get("revision_id")
        ) if webhook.payload else None
        booking_id = webhook.payload.get("booking_id") if webhook.payload else None

        if not revision_id and not booking_id:
            logger.error("No IDs in modification webhook")
            return

        logger.info(f"Booking modification: revision={revision_id}, booking={booking_id}")

        # 1. Fetch updated booking from Channex
        if revision_id:
            response = await channex.get_booking_revision(revision_id)
        else:
            response = await channex.get_booking(booking_id)

        booking = response.get("data", {}).get("attributes", {})
        booking_id = booking_id or booking.get("booking_id")
        logger.info(f"Modified booking: status={booking.get('status')}, ota={booking.get('ota_name')}")

        # 2. Find existing QloApps booking via mapping
        mapping = booking_store.get_by_channex_id(booking_id) if booking_id else None
        if not mapping:
            logger.warning(f"No QloApps mapping for Channex booking {booking_id}. Cannot modify — ack'ing to prevent retry storm.")
            if revision_id:
                await channex.ack_booking_revision(revision_id)
            return

        qloapps_order_id = mapping["qloapps_order_id"]

        # 3. Update QloApps booking (GET current → merge changes → PUT back)
        # QloApps PUT quirks:
        # - Requires id, id_property, currency, customer_detail (with ORIGINAL email), room_types with rooms
        # - Customer lookup is by email — new email = "Customer not found"
        # - Date/room changes are complex (room reallocation). POC updates guest name/phone only.
        customer = booking.get("customer", {})
        try:
            current_qloapps = await qloapps.get_booking(qloapps_order_id)
            qloapps_data = current_qloapps.get("booking", current_qloapps)

            # Build PUT payload preserving original structure
            original_cd = qloapps_data.get("associations", {}).get("customer_detail", {})
            original_rooms = qloapps_data.get("associations", {}).get("room_types", [])
            original_room = original_rooms[0] if original_rooms else {}
            original_room_detail = original_room.get("rooms", [{}])[0] if original_room.get("rooms") else {}

            # Merge guest changes (keep original email to avoid "Customer not found")
            new_firstname = customer.get("name", customer.get("first_name", original_cd.get("firstname", "")))
            new_lastname = customer.get("surname", customer.get("last_name", original_cd.get("lastname", "")))
            new_phone = customer.get("phone", original_cd.get("phone", ""))
            original_email = original_cd.get("email", "")

            ota = booking.get("ota_name", "OTA")
            unique_id = booking.get("unique_id", "")

            put_data = {
                "id": qloapps_order_id,
                "id_property": qloapps_data.get("id_property", 1),
                "currency": qloapps_data.get("currency", "BRL"),
                "source": f"Channex-{ota}",
                "associations": {
                    "customer_detail": {
                        "firstname": new_firstname,
                        "lastname": new_lastname,
                        "email": original_email,  # MUST keep original email
                        "phone": new_phone,
                    },
                    "room_types": {
                        "room_type": {
                            "id_room_type": original_room.get("id_room_type", 1),
                            "checkin_date": original_room.get("checkin_date", "").split(" ")[0],
                            "checkout_date": original_room.get("checkout_date", "").split(" ")[0],
                            "number_of_rooms": original_room.get("number_of_rooms", 1),
                            "rooms": {
                                "room": {
                                    "id_room": original_room_detail.get("id_room"),
                                    "id_hotel_booking": original_room_detail.get("id_hotel_booking", qloapps_order_id),
                                    "adults": original_room_detail.get("adults", 2),
                                    "child": original_room_detail.get("child", 0),
                                    "unit_price_without_tax": original_room_detail.get("unit_price_without_tax", 0),
                                    "total_tax": original_room_detail.get("total_tax", 0),
                                }
                            }
                        }
                    }
                }
            }

            await qloapps.update_booking(qloapps_order_id, put_data)
            logger.info(f"QloApps order {qloapps_order_id} updated: {new_firstname} {new_lastname}, phone={new_phone}")
        except Exception as update_err:
            logger.warning(f"Could not update QloApps order {qloapps_order_id}: {update_err}")
            logger.warning("Modification logged in booking_store but QloApps may be out of sync")

        # 4. Update mapping status (always, even if QloApps update failed)
        booking_store.update_status(booking_id, "modified")

        # 5. Ack in Channex
        if revision_id:
            await channex.ack_booking_revision(revision_id)
            logger.info(f"Modification {revision_id} acknowledged")
        else:
            logger.warning(f"No revision_id to ack for modification of booking {booking_id}")

        # 6. Re-sync ARI (dates may have changed)
        rooms = booking.get("rooms", [])
        if rooms:
            room = rooms[0]
            channex_room_type_id = room.get("room_type_id", "")
            qloapps_room_type_id = ROOM_TYPE_MAPPING_REVERSE.get(channex_room_type_id)
            checkin = booking.get("arrival_date")
            checkout = booking.get("departure_date")
            if qloapps_room_type_id and channex_room_type_id and checkin and checkout:
                await sync_ari_to_channex(qloapps_room_type_id, channex_room_type_id, checkin, checkout)

    except Exception as e:
        logger.error(f"Error handling Channex modification: {e}")
        logger.error(traceback.format_exc())


async def handle_channex_booking_cancelled(webhook: ChannexWebhook):
    """Process cancelled booking from Channex -> cancel in QloApps + update ARI"""
    try:
        # Channex booking_cancellation webhook uses "booking_revision_id" (not "revision_id")
        revision_id = (
            webhook.payload.get("booking_revision_id")
            or webhook.payload.get("revision_id")
        ) if webhook.payload else None
        booking_id = webhook.payload.get("booking_id") if webhook.payload else None

        if not revision_id and not booking_id:
            logger.error("No IDs in cancellation webhook")
            return

        logger.info(f"Booking cancellation: revision={revision_id}, booking={booking_id}")

        # 1. Fetch cancellation details from Channex
        if revision_id:
            response = await channex.get_booking_revision(revision_id)
        else:
            response = await channex.get_booking(booking_id)

        booking = response.get("data", {}).get("attributes", {})
        booking_id = booking_id or booking.get("booking_id")
        logger.info(f"Cancelled booking: ota={booking.get('ota_name')}")

        # 2. Find existing QloApps booking via mapping
        mapping = booking_store.get_by_channex_id(booking_id) if booking_id else None
        if not mapping:
            logger.warning(f"No QloApps mapping for Channex booking {booking_id}. Nothing to cancel — ack'ing.")
            if revision_id:
                await channex.ack_booking_revision(revision_id)
            return

        qloapps_order_id = mapping["qloapps_order_id"]

        # 3. Cancel in QloApps (best-effort — QloApps booking module may not support status changes)
        try:
            await qloapps.cancel_booking(qloapps_order_id)
            logger.info(f"QloApps order {qloapps_order_id} cancel attempted")
        except Exception as e:
            logger.warning(f"QloApps cancel failed for order {qloapps_order_id}: {e} — continuing with status update")

        # 4. Update mapping status (always — even if QloApps cancel failed)
        booking_store.update_status(booking_id, "cancelled")
        logger.info(f"Booking {booking_id} marked as cancelled in mapping store")

        # 5. Ack in Channex
        if revision_id:
            await channex.ack_booking_revision(revision_id)
            logger.info(f"Cancellation {revision_id} acknowledged")

        # 6. Re-sync ARI (rooms are now free)
        rooms = booking.get("rooms", [])
        if rooms:
            room = rooms[0]
            channex_room_type_id = room.get("room_type_id", "")
            qloapps_room_type_id = ROOM_TYPE_MAPPING_REVERSE.get(channex_room_type_id)
            checkin = booking.get("arrival_date")
            checkout = booking.get("departure_date")
            if qloapps_room_type_id and channex_room_type_id and checkin and checkout:
                logger.info("Re-syncing ARI after cancellation (rooms freed)...")
                await sync_ari_to_channex(qloapps_room_type_id, channex_room_type_id, checkin, checkout)

    except Exception as e:
        logger.error(f"Error handling Channex cancellation: {e}")
        logger.error(traceback.format_exc())


async def handle_qloapps_booking_created(webhook: QloAppsWebhook):
    """Process new booking from QloApps -> update Channex availability"""
    try:
        order_id = webhook.data.get("order_id")
        rooms = webhook.data.get("rooms", [])

        logger.info(f"QloApps booking created: order {order_id}")
        logger.info(f"Booking data: customer={webhook.data.get('customer_firstname')} {webhook.data.get('customer_lastname')}, rooms={len(rooms)}")

        if not rooms:
            logger.warning("No room data in webhook - module may need update")
            return

        for room in rooms:
            qloapps_room_type_id = int(room.get("id_room_type", 0))
            checkin = room.get("checkin_date", "").split(" ")[0]
            checkout = room.get("checkout_date", "").split(" ")[0]

            channex_room_type = ROOM_TYPE_MAPPING.get(qloapps_room_type_id)

            if not channex_room_type:
                logger.warning(f"Unknown room type ID: {qloapps_room_type_id}")
                continue

            logger.info(f"Room booked: type={qloapps_room_type_id}, {checkin} to {checkout}")

            # Get current availability from QloApps
            await sync_ari_to_channex(qloapps_room_type_id, channex_room_type, checkin, checkout)

    except Exception as e:
        logger.error(f"Error handling QloApps booking: {e}")
        logger.error(traceback.format_exc())


async def handle_qloapps_booking_updated(webhook: QloAppsWebhook):
    """Process updated booking from QloApps -> re-sync availability"""
    try:
        order_id = webhook.data.get("order_id")
        rooms = webhook.data.get("rooms", [])

        logger.info(f"QloApps booking updated: order {order_id}")

        for room in rooms:
            qloapps_room_type_id = int(room.get("id_room_type", 0))
            checkin = room.get("checkin_date", "").split(" ")[0]
            checkout = room.get("checkout_date", "").split(" ")[0]

            channex_room_type = ROOM_TYPE_MAPPING.get(qloapps_room_type_id)
            if not channex_room_type:
                continue

            await sync_ari_to_channex(qloapps_room_type_id, channex_room_type, checkin, checkout)

    except Exception as e:
        logger.error(f"Error handling QloApps booking update: {e}")
        logger.error(traceback.format_exc())


async def handle_qloapps_booking_cancelled(webhook: QloAppsWebhook):
    """Process cancelled booking from QloApps -> re-sync availability (rooms freed up)"""
    try:
        order_id = webhook.data.get("order_id")
        rooms = webhook.data.get("rooms", [])

        logger.info(f"QloApps booking cancelled: order {order_id}")

        for room in rooms:
            qloapps_room_type_id = int(room.get("id_room_type", 0))
            checkin = room.get("checkin_date", "").split(" ")[0]
            checkout = room.get("checkout_date", "").split(" ")[0]

            channex_room_type = ROOM_TYPE_MAPPING.get(qloapps_room_type_id)
            if not channex_room_type:
                continue

            # Re-sync: availability should now be higher since rooms are freed
            await sync_ari_to_channex(qloapps_room_type_id, channex_room_type, checkin, checkout)

    except Exception as e:
        logger.error(f"Error handling QloApps booking cancellation: {e}")
        logger.error(traceback.format_exc())


# === Sync Functions ===

async def sync_ari_to_channex(
    qloapps_room_type_id: int,
    channex_room_type_id: str,
    date_from: str,
    date_to: str
):
    """
    Query QloApps for current ARI and push to Channex.

    Syncs both:
    - Availability (room count) via POST /availability
    - Rates + restrictions via POST /restrictions

    Called on booking create, update, and cancel.
    Always queries QloApps for the definitive data (not incremental).
    """
    # Retry with backoff: QloApps webhook fires while PHP still holds DB locks,
    # so the hotel_ari endpoint may be unavailable for several seconds
    max_retries = 3
    delays = [5, 10, 20]  # seconds between retries

    for attempt in range(max_retries):
        try:
            wait = delays[attempt]
            logger.info(f"Syncing ARI: room_type={qloapps_room_type_id}, {date_from} to {date_to} (attempt {attempt + 1}/{max_retries}, waiting {wait}s)")
            await asyncio.sleep(wait)

            # 1. Get current ARI from QloApps (single call returns availability AND prices)
            ari_data = await qloapps.get_availability(
                hotel_id=1,
                date_from=date_from,
                date_to=date_to
            )

            logger.info(f"QloApps ARI response: {ari_data}")

            # 2. Parse and push availability
            available_count = parse_qloapps_availability(ari_data, qloapps_room_type_id)

            if available_count is None:
                logger.warning(f"Could not parse availability for room type {qloapps_room_type_id}")
                logger.warning("Setting availability to 0 as safe default (prevents overbooking)")
                available_count = 0

            avail_values = [{
                "property_id": settings.channex_property_id,
                "room_type_id": channex_room_type_id,
                "date_from": date_from,
                "date_to": date_to,
                "availability": max(0, available_count),
            }]

            result = await channex.update_availability(avail_values)
            logger.info(f"Channex availability updated: {available_count} rooms, {date_from} to {date_to}")

            # 3. Parse and push rate + restrictions
            rate = parse_qloapps_rate(ari_data, qloapps_room_type_id)
            channex_rate_plan = RATE_PLAN_MAPPING.get(qloapps_room_type_id)

            if rate and rate > 0 and channex_rate_plan:
                restriction_values = [{
                    "property_id": settings.channex_property_id,
                    "rate_plan_id": channex_rate_plan,
                    "date_from": date_from,
                    "date_to": date_to,
                    "rate": int(rate * 100),  # Channex expects cents
                    **DEFAULT_RESTRICTIONS,
                }]

                rate_result = await channex.update_restrictions(restriction_values)
                logger.info(f"Channex rate updated: R${rate:.2f}/night ({int(rate*100)} cents), {date_from} to {date_to}")
            else:
                if not rate or rate <= 0:
                    logger.warning(f"No valid rate for room type {qloapps_room_type_id}, skipping rate sync")
                if not channex_rate_plan:
                    logger.warning(f"No rate plan mapping for room type {qloapps_room_type_id}, skipping rate sync")

            return  # success

        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Attempt {attempt + 1} failed: {e} — retrying...")
            else:
                logger.error(f"All {max_retries} attempts failed syncing ARI to Channex")
                logger.error(f"Last error: {e}")
                logger.error(traceback.format_exc())


def parse_qloapps_availability(ari_data: dict, room_type_id: int) -> dict:
    """
    Parse QloApps hotel_ari response to extract available room count.

    QloApps returns data in this format:
    {
        "hotel_ari": {
            "room_types": [
                {
                    "id_room_type": 1,
                    "name": "General Rooms",
                    "rooms": {
                        "available": {"1": {...}, "2": {...}}  // each key = a room
                    }
                }
            ]
        }
    }

    The number of available rooms = number of keys in rooms.available.
    Note: This gives total availability for the DATE RANGE, not per-date.
    """
    try:
        hotel_ari = ari_data.get("hotel_ari", {})
        room_types = hotel_ari.get("room_types", [])

        for rt in room_types:
            rt_id = int(rt.get("id_room_type", 0))
            if rt_id == room_type_id:
                available_rooms = rt.get("rooms", {}).get("available", {})
                count = len(available_rooms)
                logger.info(f"Room type {room_type_id} ({rt.get('name', '?')}): {count} rooms available")
                return count

        logger.warning(f"Room type {room_type_id} not found in ARI response")
        return None

    except Exception as e:
        logger.error(f"Error parsing QloApps availability: {e}")
        return None


def parse_qloapps_rate(ari_data: dict, room_type_id: int) -> float:
    """
    Parse QloApps hotel_ari response to extract per-night rate.

    Returns base_price_with_tax (tax-inclusive nightly rate).
    This is the price guests see on OTAs.
    Returns None if room type not found.
    """
    try:
        hotel_ari = ari_data.get("hotel_ari", {})
        room_types = hotel_ari.get("room_types", [])

        for rt in room_types:
            rt_id = int(rt.get("id_room_type", 0))
            if rt_id == room_type_id:
                rate = float(rt.get("base_price_with_tax", 0))
                logger.info(f"Room type {room_type_id} ({rt.get('name', '?')}): R${rate:.2f}/night")
                return rate

        logger.warning(f"Room type {room_type_id} not found in ARI response for rate")
        return None

    except Exception as e:
        logger.error(f"Error parsing QloApps rate: {e}")
        return None


# === Transform Functions ===

def transform_channex_to_qloapps(channex_booking: dict) -> dict:
    """Transform Channex booking format to QloApps format.

    Note: Channex customer fields may vary (name/surname vs single name).
    The debug endpoint /webhook/channex/debug logs the real format.
    """
    # Extract guest info
    # Channex docs: customer has name, surname, mail, phone
    # Fallback: if only "name" exists, split on space
    customer = channex_booking.get("customer", {})
    firstname = customer.get("name", customer.get("first_name", ""))
    lastname = customer.get("surname", customer.get("last_name", ""))

    if not firstname and not lastname:
        # Last resort: try full_name or just "Guest"
        full_name = customer.get("full_name", "Guest Unknown")
        parts = full_name.split(" ", 1)
        firstname = parts[0]
        lastname = parts[1] if len(parts) > 1 else ""

    email = customer.get("mail", customer.get("email", ""))
    phone = customer.get("phone", "")

    # Extract room info
    rooms = channex_booking.get("rooms", [])
    room = rooms[0] if rooms else {}

    if len(rooms) > 1:
        logger.warning(f"Multi-room booking ({len(rooms)} rooms) — only first room will be processed")

    # Map Channex room_type_id to QloApps id_room_type
    channex_room_type = room.get("room_type_id", "")
    qloapps_room_type = ROOM_TYPE_MAPPING_REVERSE.get(channex_room_type, 1)

    if channex_room_type and not ROOM_TYPE_MAPPING_REVERSE.get(channex_room_type):
        logger.warning(f"Unknown Channex room_type_id: {channex_room_type}, defaulting to QloApps type 1")

    # Dates
    checkin = channex_booking.get("arrival_date", "")
    checkout = channex_booking.get("departure_date", "")

    # Price
    total = channex_booking.get("amount", "0")
    currency = channex_booking.get("currency", "BRL")

    # Source/OTA
    ota = channex_booking.get("ota_name", "OTA")
    unique_id = channex_booking.get("unique_id", "")

    # Tax split: POC uses 80/20 estimate
    total_float = float(total)
    price_without_tax = round(total_float * 0.8, 2)
    tax = round(total_float * 0.2, 2)
    if total_float > 0:
        logger.warning(f"Tax split is estimated (80/20): base={price_without_tax}, tax={tax}")

    return {
        "id_property": 1,
        "currency": currency,
        "booking_status": 1,  # API_BOOKING_STATUS_NEW
        "payment_status": 1,
        "source": f"Channex-{ota}",
        "remark": f"OTA: {ota} | Ref: {unique_id}",
        "associations": {
            "customer_detail": {
                "firstname": firstname,
                "lastname": lastname,
                "email": email,
                "phone": phone,
            },
            "price_details": {
                "total_paid": "0",
                "total_price_with_tax": str(total),
            },
            "room_types": {
                "room_type": {
                    "id_room_type": qloapps_room_type,
                    "checkin_date": checkin,
                    "checkout_date": checkout,
                    "number_of_rooms": 1,
                    "rooms": {
                        "room": {
                            "adults": room.get("occupancy", {}).get("adults", 2),
                            "child": room.get("occupancy", {}).get("children", 0),
                            "unit_price_without_tax": str(price_without_tax),
                            "total_tax": str(tax),
                        }
                    }
                }
            }
        }
    }


def extract_qloapps_order_id(response: dict) -> int:
    """Extract order ID from QloApps create booking response."""
    try:
        booking = response.get("booking", response)
        if isinstance(booking, dict):
            order_id = booking.get("id")
            if order_id:
                return int(order_id)
        # Fallback: check for order key
        order_id = response.get("id")
        if order_id:
            return int(order_id)
        logger.warning(f"Could not extract order_id from QloApps response: {json.dumps(response, default=str)[:500]}")
        return 0
    except Exception as e:
        logger.error(f"Error extracting order_id: {e}")
        return 0


# === Utility Endpoints ===

@app.get("/health", tags=["Status"])
async def health():
    """
    Verifica se o middleware esta funcionando.

    Retorna status dos servicos conectados (QloApps e Channex).
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "qloapps": settings.qloapps_url,
            "channex": settings.channex_url,
        }
    }


@app.get("/", tags=["Status"])
async def root():
    """Pagina inicial com links para os endpoints."""
    return {
        "name": "AI-PMS Middleware",
        "version": "1.0.0",
        "endpoints": {
            "webhooks": ["/webhook/channex", "/webhook/qloapps"],
            "health": "/health",
            "docs": "/docs",
        }
    }


# === Debug Endpoints ===

@app.post("/webhook/channex/debug", tags=["Debug"])
async def webhook_channex_debug(request: Request):
    """
    Endpoint temporario para capturar o formato EXATO do webhook do Channex.

    Aceita qualquer JSON, loga completo, retorna 200.
    Usar para validar antes de confiar no model ChannexWebhook.
    """
    body = await request.json()
    logger.info(f"=== RAW CHANNEX WEBHOOK ===")
    logger.info(json.dumps(body, indent=2, default=str))
    logger.info(f"=== END RAW WEBHOOK ===")
    return {"status": "received_debug", "body": body}


@app.get("/bookings/mapping", tags=["Debug"])
async def list_booking_mappings():
    """
    Mostra todos os mapeamentos Channex <-> QloApps.

    Util pra verificar se bookings estao sendo rastreados corretamente.
    """
    return booking_store.get_all()


@app.get("/bookings/channex/feed", tags=["Debug"])
async def channex_booking_feed():
    """
    Mostra revisions de booking nao-confirmadas no Channex.

    Se tiver items aqui, significa que o middleware ainda nao processou/ack'd.
    """
    return await channex.get_booking_revision_feed(settings.channex_property_id)


# === Manual Sync Endpoints (for testing) ===

@app.post("/sync/availability", tags=["Sync Manual (para testar)"])
async def sync_availability_manual(
    room_type_id: int,
    date_from: str,
    date_to: str,
    availability: int
):
    """
    Enviar disponibilidade manualmente pro Channex.

    Exemplo: "Quarto tipo 1 tem 3 unidades disponiveis de 01/02 a 05/02"

    - **room_type_id**: ID do tipo de quarto no QloApps (1=General, 2=Delux, 3=Executive, 4=Luxury, 11=Upper Laker)
    - **date_from**: Data inicio (formato: 2026-02-01)
    - **date_to**: Data fim (formato: 2026-02-05)
    - **availability**: Quantos quartos disponiveis
    """
    channex_room_type = ROOM_TYPE_MAPPING.get(room_type_id)

    if not channex_room_type:
        raise HTTPException(400, f"Unknown room_type_id: {room_type_id}")

    values = [{
        "property_id": settings.channex_property_id,
        "room_type_id": channex_room_type,
        "date_from": date_from,
        "date_to": date_to,
        "availability": availability,
    }]

    result = await channex.update_availability(values)
    return {"status": "ok", "result": result}


@app.post("/sync/rate", tags=["Sync Manual (para testar)"])
async def sync_rate_manual(
    room_type_id: int,
    date_from: str,
    date_to: str,
    rate: float
):
    """
    Enviar tarifa manualmente pro Channex.

    Exemplo: "Quarto tipo 1 custa R$500 por noite de 01/02 a 05/02"

    - **room_type_id**: ID do tipo de quarto no QloApps
    - **date_from**: Data inicio (formato: 2026-02-01)
    - **date_to**: Data fim (formato: 2026-02-05)
    - **rate**: Valor por noite em reais (ex: 500.00)
    """
    channex_rate_plan = RATE_PLAN_MAPPING.get(room_type_id)

    if not channex_rate_plan:
        raise HTTPException(400, f"Unknown room_type_id: {room_type_id}")

    values = [{
        "property_id": settings.channex_property_id,
        "rate_plan_id": channex_rate_plan,
        "date_from": date_from,
        "date_to": date_to,
        "rate": int(rate * 100),  # Channex expects cents
    }]

    result = await channex.update_restrictions(values)
    return {"status": "ok", "result": result}


@app.post("/sync/restrictions", tags=["Sync Manual (para testar)"])
async def sync_restrictions_manual(
    room_type_id: int,
    date_from: str,
    date_to: str,
    min_stay_arrival: int = 1,
    stop_sell: bool = False,
    closed_to_arrival: bool = False,
    closed_to_departure: bool = False,
):
    """
    Enviar restricoes manualmente pro Channex.

    Controla como o quarto aparece nas OTAs pra um periodo especifico.

    - **room_type_id**: ID do tipo de quarto no QloApps
    - **date_from**: Data inicio (formato: 2026-02-01)
    - **date_to**: Data fim (formato: 2026-02-05)
    - **min_stay_arrival**: Minimo de noites se check-in nessa data (default: 1)
    - **stop_sell**: Parar vendas nesse periodo (default: false)
    - **closed_to_arrival**: Nao aceitar check-in nessas datas (default: false)
    - **closed_to_departure**: Nao aceitar check-out nessas datas (default: false)
    """
    channex_rate_plan = RATE_PLAN_MAPPING.get(room_type_id)

    if not channex_rate_plan:
        raise HTTPException(400, f"Unknown room_type_id: {room_type_id}")

    values = [{
        "property_id": settings.channex_property_id,
        "rate_plan_id": channex_rate_plan,
        "date_from": date_from,
        "date_to": date_to,
        "min_stay_arrival": min_stay_arrival,
        "stop_sell": stop_sell,
        "closed_to_arrival": closed_to_arrival,
        "closed_to_departure": closed_to_departure,
    }]

    result = await channex.update_restrictions(values)
    return {"status": "ok", "result": result}


@app.post("/sync/full", tags=["Sync Manual (para testar)"])
async def sync_full_from_qloapps(room_type_id: int, date_from: str, date_to: str):
    """
    Sincronizar ARI completo (disponibilidade + tarifa + restricoes) do QloApps pro Channex.

    Consulta o QloApps pra saber quantos quartos estao disponiveis e o preco,
    e envia tudo pro Channex.

    **Precisa do QloApps rodando em localhost:8080.**

    - **room_type_id**: ID do tipo de quarto no QloApps
    - **date_from**: Data inicio (formato: 2026-02-01)
    - **date_to**: Data fim (formato: 2026-02-05)
    """
    channex_room_type = ROOM_TYPE_MAPPING.get(room_type_id)

    if not channex_room_type:
        raise HTTPException(400, f"Unknown room_type_id: {room_type_id}")

    await sync_ari_to_channex(room_type_id, channex_room_type, date_from, date_to)
    return {"status": "ok", "room_type_id": room_type_id, "date_from": date_from, "date_to": date_to}


@app.get("/bookings/channex", tags=["Consultar Reservas"])
async def list_channex_bookings(status: Optional[str] = None):
    """
    Ver reservas no Channex.

    Mostra todas as reservas que o Channex recebeu (de OTAs).

    - **status** (opcional): Filtrar por status (new, modified, cancelled)
    """
    return await channex.list_bookings(
        property_id=settings.channex_property_id,
        status=status
    )


@app.get("/bookings/qloapps", tags=["Consultar Reservas"])
async def list_qloapps_bookings():
    """
    Ver reservas no QloApps.

    Mostra todas as reservas que estao no PMS (QloApps).

    **Precisa do QloApps rodando em localhost:8080.**
    """
    return await qloapps.list_bookings()
