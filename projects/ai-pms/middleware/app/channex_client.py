"""
Channex API Client
https://docs.channex.io/
"""
import httpx
from typing import Optional
from .config import settings


class ChannexClient:
    def __init__(self):
        self.base_url = settings.channex_url
        self.headers = {
            "Content-Type": "application/json",
            "user-api-key": settings.channex_api_key,
        }

    async def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json() if response.content else {}

    # === Bookings ===

    async def get_booking(self, booking_id: str) -> dict:
        """Get full booking details by ID"""
        return await self._request("GET", f"/bookings/{booking_id}")

    async def ack_booking(self, booking_id: str) -> dict:
        """Acknowledge a booking (mark as received)"""
        return await self._request("POST", f"/bookings/{booking_id}/ack")

    async def list_bookings(
        self,
        property_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> dict:
        """List bookings with optional filters"""
        params = {}
        if property_id:
            params["filter[property_id]"] = property_id
        if status:
            params["filter[status]"] = status
        return await self._request("GET", "/bookings", params=params)

    # === ARI (Availability, Rates, Inventory) ===

    async def update_restrictions(self, values: list[dict]) -> dict:
        """
        Update availability/rates/restrictions

        values example:
        [{
            "property_id": "uuid",
            "room_type_id": "uuid",
            "rate_plan_id": "uuid",
            "date": "2026-01-25",
            "availability": 5,
            "rate": "1000.00",  # Must be string!
            "min_stay_arrival": 1
        }]
        """
        return await self._request("POST", "/restrictions", json={"values": values})

    # === Webhooks ===

    async def create_webhook(
        self,
        property_id: str,
        callback_url: str,
        event_mask: str = "booking",
        is_active: bool = True,
        send_data: bool = True,
        headers: Optional[dict] = None
    ) -> dict:
        """Create a webhook subscription"""
        payload = {
            "property_id": property_id,
            "callback_url": callback_url,
            "event_mask": event_mask,
            "is_active": is_active,
            "send_data": send_data,
        }
        if headers:
            payload["headers"] = headers
        return await self._request("POST", "/webhooks", json=payload)

    async def list_webhooks(self) -> dict:
        """List all webhooks"""
        return await self._request("GET", "/webhooks")

    async def delete_webhook(self, webhook_id: str) -> dict:
        """Delete a webhook"""
        return await self._request("DELETE", f"/webhooks/{webhook_id}")

    async def test_webhook(self, callback_url: str) -> dict:
        """Test a webhook endpoint"""
        return await self._request("POST", "/webhooks/test", json={"callback_url": callback_url})


# Singleton instance
channex = ChannexClient()
