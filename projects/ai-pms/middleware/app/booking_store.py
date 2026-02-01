"""
File-based booking ID mapping (Channex <-> QloApps).

Stores a JSON file that tracks which Channex booking corresponds to which
QloApps order. Enables idempotency, modification lookup, and cancellation lookup.
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"
BOOKINGS_FILE = DATA_DIR / "bookings.json"


class BookingStore:
    def __init__(self, filepath: Path = BOOKINGS_FILE):
        self.filepath = filepath
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self.filepath.exists():
            self._write({})

    def _read(self) -> dict:
        with open(self.filepath, "r") as f:
            return json.load(f)

    def _write(self, data: dict):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def save_booking(
        self,
        channex_booking_id: str,
        qloapps_order_id: int,
        **extra
    ) -> dict:
        """Save a new booking mapping. Returns the entry."""
        data = self._read()
        now = datetime.now().isoformat()
        entry = {
            "qloapps_order_id": qloapps_order_id,
            "channex_booking_id": channex_booking_id,
            "status": "new",
            "created_at": now,
            "updated_at": now,
            **extra,
        }
        data[channex_booking_id] = entry
        self._write(data)
        logger.info(f"Booking mapping saved: channex={channex_booking_id} -> qloapps={qloapps_order_id}")
        return entry

    def get_by_channex_id(self, channex_booking_id: str) -> Optional[dict]:
        """Lookup a QloApps order by Channex booking ID."""
        data = self._read()
        return data.get(channex_booking_id)

    def update_status(self, channex_booking_id: str, status: str):
        """Update the status of a tracked booking."""
        data = self._read()
        if channex_booking_id in data:
            data[channex_booking_id]["status"] = status
            data[channex_booking_id]["updated_at"] = datetime.now().isoformat()
            self._write(data)
            logger.info(f"Booking {channex_booking_id} status -> {status}")

    def exists(self, channex_booking_id: str) -> bool:
        """Check if a Channex booking has already been processed."""
        data = self._read()
        return channex_booking_id in data

    def get_all(self) -> dict:
        """Return all booking mappings (for debug endpoint)."""
        return self._read()


booking_store = BookingStore()
