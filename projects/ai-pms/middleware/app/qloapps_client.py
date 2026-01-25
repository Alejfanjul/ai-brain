"""
QloApps API Client (XML-based)
"""
import httpx
import xmltodict
from typing import Optional
from .config import settings


class QloAppsClient:
    def __init__(self):
        self.base_url = f"{settings.qloapps_url}/webservice/dispatcher.php"
        self.api_key = settings.qloapps_api_key

    async def _request(
        self,
        method: str,
        resource: str,
        resource_id: Optional[int] = None,
        data: Optional[dict] = None,
        output_format: str = "JSON"
    ) -> dict:
        """Make request to QloApps API"""
        url = f"{self.base_url}?url={resource}"
        if resource_id:
            url += f"/{resource_id}"
        url += f"&output_format={output_format}"

        auth = (self.api_key, "")

        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, auth=auth)
            elif method == "POST":
                xml_data = self._dict_to_xml(resource, data)
                response = await client.post(
                    url,
                    auth=auth,
                    content=xml_data,
                    headers={"Content-Type": "application/xml"}
                )
            elif method == "PUT":
                xml_data = self._dict_to_xml(resource, data)
                response = await client.put(
                    url,
                    auth=auth,
                    content=xml_data,
                    headers={"Content-Type": "application/xml"}
                )
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()

            if output_format == "JSON":
                return response.json() if response.content else {}
            else:
                return xmltodict.parse(response.content)

    def _dict_to_xml(self, resource: str, data: dict) -> str:
        """Convert dict to QloApps XML format"""
        # Singular form of resource name
        singular = resource.rstrip('s')
        wrapper = {"qloapps": {singular: data}}
        return xmltodict.unparse(wrapper, pretty=True)

    # === Bookings ===

    async def get_booking(self, booking_id: int) -> dict:
        """Get booking by ID"""
        return await self._request("GET", "bookings", resource_id=booking_id)

    async def list_bookings(self) -> dict:
        """List all bookings"""
        return await self._request("GET", "bookings")

    async def create_booking(self, booking_data: dict) -> dict:
        """
        Create a new booking

        booking_data example:
        {
            "id_property": 1,
            "currency": "BRL",
            "booking_status": 1,
            "payment_status": 1,
            "source": "Channex-Booking.com",
            "associations": {
                "customer_detail": {
                    "firstname": "Maria",
                    "lastname": "Santos",
                    "email": "maria@test.com",
                    "phone": "11999998888"
                },
                "price_details": {
                    "total_paid": "0",
                    "total_price_with_tax": "900.00"
                },
                "room_types": {
                    "room_type": {
                        "id_room_type": 1,
                        "checkin_date": "2026-03-10",
                        "checkout_date": "2026-03-12",
                        "number_of_rooms": 1,
                        "rooms": {
                            "room": {
                                "adults": 2,
                                "child": 0,
                                "unit_price_without_tax": "720.00",
                                "total_tax": "180.00"
                            }
                        }
                    }
                }
            }
        }
        """
        return await self._request("POST", "bookings", data=booking_data)

    # === Availability ===

    async def get_availability(
        self,
        hotel_id: int = 1,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> dict:
        """Get hotel availability (ARI)"""
        # hotel_ari endpoint requires special handling
        url = f"{self.base_url}?url=hotel_ari&id_hotel={hotel_id}&output_format=JSON"
        if date_from:
            url += f"&date_from={date_from}"
        if date_to:
            url += f"&date_to={date_to}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, auth=(self.api_key, ""))
            response.raise_for_status()
            return response.json() if response.content else {}

    # === Room Types ===

    async def list_room_types(self) -> dict:
        """List all room types"""
        return await self._request("GET", "room_types")

    async def get_room_type(self, room_type_id: int) -> dict:
        """Get room type by ID"""
        return await self._request("GET", "room_types", resource_id=room_type_id)

    # === Customers ===

    async def create_customer(self, customer_data: dict) -> dict:
        """Create a new customer"""
        return await self._request("POST", "customers", data=customer_data)

    async def find_customer_by_email(self, email: str) -> Optional[dict]:
        """Find customer by email"""
        # QloApps doesn't have native filter, need to list and search
        customers = await self._request("GET", "customers")
        # This is inefficient but QloApps API is limited
        # In production, query database directly
        return None  # TODO: implement search


# Singleton instance
qloapps = QloAppsClient()
