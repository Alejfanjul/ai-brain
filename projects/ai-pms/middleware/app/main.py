"""
AI-PMS Middleware
FastAPI application that syncs QloApps <-> Channex

Endpoints:
- POST /webhook/channex  - Receives webhooks from Channex (OTA bookings)
- POST /webhook/qloapps  - Receives webhooks from QloApps module (direct bookings)
- GET  /health           - Health check
"""
import logging
import traceback
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional

from .config import settings, ROOM_TYPE_MAPPING, ROOM_TYPE_MAPPING_REVERSE, RATE_PLAN_MAPPING
from .channex_client import channex
from .qloapps_client import qloapps

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI-PMS Middleware",
    description="Syncs QloApps PMS with Channex Channel Manager",
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

@app.post("/webhook/channex")
async def webhook_channex(webhook: ChannexWebhook, background_tasks: BackgroundTasks):
    """
    Receive webhook from Channex.
    Handles: booking_new, booking_modification, booking_cancellation
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


@app.post("/webhook/qloapps")
async def webhook_qloapps(webhook: QloAppsWebhook, background_tasks: BackgroundTasks):
    """
    Receive webhook from QloApps module.
    Handles: booking.created, booking.updated, booking.cancelled
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
        booking_id = webhook.payload.get("booking_id") if webhook.payload else None
        if not booking_id:
            logger.error("No booking_id in Channex webhook payload")
            return

        # 1. Fetch full booking details from Channex
        logger.info(f"Fetching booking {booking_id} from Channex...")
        booking_response = await channex.get_booking(booking_id)
        booking = booking_response.get("data", {}).get("attributes", {})

        # 2. Transform Channex booking to QloApps format
        qloapps_booking = transform_channex_to_qloapps(booking)

        # 3. Create booking in QloApps
        logger.info(f"Creating booking in QloApps...")
        result = await qloapps.create_booking(qloapps_booking)
        logger.info(f"Booking created in QloApps: {result}")

        # 4. Acknowledge booking in Channex
        await channex.ack_booking(booking_id)
        logger.info(f"Booking {booking_id} acknowledged in Channex")

    except Exception as e:
        logger.error(f"Error handling Channex booking: {e}")


async def handle_channex_booking_modified(webhook: ChannexWebhook):
    """Process modified booking from Channex"""
    logger.info("Booking modification - TODO: implement update logic")
    # TODO: Find existing booking in QloApps and update


async def handle_channex_booking_cancelled(webhook: ChannexWebhook):
    """Process cancelled booking from Channex"""
    logger.info("Booking cancellation - TODO: implement cancel logic")
    # TODO: Find existing booking in QloApps and cancel


async def handle_qloapps_booking_created(webhook: QloAppsWebhook):
    """Process new booking from QloApps -> update Channex ARI"""
    try:
        order_id = webhook.data.get("order_id")
        rooms = webhook.data.get("rooms", [])

        logger.info(f"QloApps booking created: order {order_id}")
        logger.info(f"Booking data: customer={webhook.data.get('customer_firstname')} {webhook.data.get('customer_lastname')}, rooms={len(rooms)}")

        if not rooms:
            logger.warning("No room data in webhook - module may need update")
            return

        # Process each room booked
        for room in rooms:
            qloapps_room_type_id = int(room.get("id_room_type", 0))
            checkin = room.get("checkin_date", "").split(" ")[0]  # Remove time if present
            checkout = room.get("checkout_date", "").split(" ")[0]

            # Map to Channex IDs
            channex_room_type = ROOM_TYPE_MAPPING.get(qloapps_room_type_id)
            channex_rate_plan = RATE_PLAN_MAPPING.get(qloapps_room_type_id)

            if not channex_room_type:
                logger.warning(f"Unknown room type ID: {qloapps_room_type_id}")
                continue

            logger.info(f"Room booked: type={qloapps_room_type_id}, {checkin} to {checkout}")

            # Generate date range for ARI update
            from datetime import datetime as dt
            start = dt.strptime(checkin, "%Y-%m-%d")
            end = dt.strptime(checkout, "%Y-%m-%d")

            dates_to_update = []
            current = start
            while current < end:
                dates_to_update.append(current.strftime("%Y-%m-%d"))
                current += timedelta(days=1)

            logger.info(f"Dates affected: {dates_to_update}")
            logger.info(f"Channex mapping: room_type={channex_room_type}, rate_plan={channex_rate_plan}")

            # TODO: Get actual availability from QloApps and push to Channex
            # For now, just log that we would update
            logger.info(f"SUCCESS: Would sync {len(dates_to_update)} dates to Channex for room type {qloapps_room_type_id}")

    except Exception as e:
        logger.error(f"Error handling QloApps booking: {e}")
        logger.error(traceback.format_exc())


async def handle_qloapps_booking_updated(webhook: QloAppsWebhook):
    """Process updated booking from QloApps"""
    logger.info("QloApps booking updated - checking if ARI needs update")


async def handle_qloapps_booking_cancelled(webhook: QloAppsWebhook):
    """Process cancelled booking from QloApps -> update Channex ARI (increase availability)"""
    logger.info("QloApps booking cancelled - TODO: increase Channex availability")


# === Transform Functions ===

def transform_channex_to_qloapps(channex_booking: dict) -> dict:
    """Transform Channex booking format to QloApps format"""

    # Extract guest info
    customer = channex_booking.get("customer", {})
    name_parts = customer.get("name", "Guest Unknown").split(" ", 1)
    firstname = name_parts[0]
    lastname = name_parts[1] if len(name_parts) > 1 else ""

    # Extract room info
    rooms = channex_booking.get("rooms", [])
    room = rooms[0] if rooms else {}

    # Map Channex room_type_id to QloApps id_room_type
    channex_room_type = room.get("room_type_id", "")
    qloapps_room_type = ROOM_TYPE_MAPPING_REVERSE.get(channex_room_type, 1)

    # Dates
    checkin = channex_booking.get("arrival_date", "")
    checkout = channex_booking.get("departure_date", "")

    # Price
    total = channex_booking.get("amount", "0")
    currency = channex_booking.get("currency", "BRL")

    # Source/OTA
    ota = channex_booking.get("ota_name", "OTA")

    return {
        "id_property": 1,
        "currency": currency,
        "booking_status": 1,  # API_BOOKING_STATUS_NEW
        "payment_status": 1,
        "source": f"Channex-{ota}",
        "remark": f"OTA Booking via Channex",
        "associations": {
            "customer_detail": {
                "firstname": firstname,
                "lastname": lastname,
                "email": customer.get("email", ""),
                "phone": customer.get("phone", ""),
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
                            "unit_price_without_tax": str(float(total) * 0.8),  # Estimate
                            "total_tax": str(float(total) * 0.2),  # Estimate
                        }
                    }
                }
            }
        }
    }


# === Utility Endpoints ===

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "qloapps": settings.qloapps_url,
            "channex": settings.channex_url,
        }
    }


@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "name": "AI-PMS Middleware",
        "version": "1.0.0",
        "endpoints": {
            "webhooks": ["/webhook/channex", "/webhook/qloapps"],
            "health": "/health",
            "docs": "/docs",
        }
    }


# === Manual Sync Endpoints (for testing) ===

@app.post("/sync/ari")
async def sync_ari_to_channex(
    room_type_id: int,
    date: str,
    availability: int,
    rate: float
):
    """Manually push ARI update to Channex"""
    channex_room_type = ROOM_TYPE_MAPPING.get(room_type_id)
    channex_rate_plan = RATE_PLAN_MAPPING.get(room_type_id)

    if not channex_room_type or not channex_rate_plan:
        raise HTTPException(400, f"Unknown room_type_id: {room_type_id}")

    values = [{
        "property_id": settings.channex_property_id,
        "room_type_id": channex_room_type,
        "rate_plan_id": channex_rate_plan,
        "date": date,
        "availability": availability,
        "rate": str(rate),  # Must be string!
    }]

    result = await channex.update_restrictions(values)
    return {"status": "ok", "result": result}


@app.get("/bookings/channex")
async def list_channex_bookings(status: Optional[str] = None):
    """List bookings from Channex"""
    return await channex.list_bookings(
        property_id=settings.channex_property_id,
        status=status
    )


@app.get("/bookings/qloapps")
async def list_qloapps_bookings():
    """List bookings from QloApps"""
    return await qloapps.list_bookings()
