from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # QloApps
    qloapps_url: str = "http://localhost:8080"
    qloapps_api_key: str = "Q4D4TJJUN8DNHZL6GTZY2VQ493V2DMH9"

    # Channex
    channex_url: str = "https://staging.channex.io/api/v1"
    channex_api_key: str = "uTdTdIa1S+kXozFtM8wGtESiMtrzb7aRSZI50Io7rYEsS+EKApvdHjvvx+mqP09v"
    channex_property_id: str = "7c504651-9b33-48bc-9896-892c351f3736"

    # Webhook security
    webhook_secret: str = ""

    class Config:
        env_file = ".env"


settings = Settings()


# Room type mapping: QloApps ID -> Channex UUID
ROOM_TYPE_MAPPING = {
    1: "3e19102f-29fd-4597-8ef1-6037703056eb",   # General Rooms
    2: "329d23da-9238-4b58-b0a0-a7a294e7e024",   # Delux Rooms
    3: "0dd44d4a-38f4-49db-baa9-b837a6d37afe",   # Executive Rooms
    4: "54887bb9-aecb-4970-9011-c5e00106bc88",   # Luxury Rooms
    11: "2d655afd-60fd-42ac-9d05-4cddce65bc88",  # Upper Laker
}

# Reverse mapping: Channex UUID -> QloApps ID
ROOM_TYPE_MAPPING_REVERSE = {v: k for k, v in ROOM_TYPE_MAPPING.items()}

# Rate plan mapping: QloApps room type ID -> Channex rate plan UUID
RATE_PLAN_MAPPING = {
    1: "69d0f921-5ec5-4712-a50c-69f1853705a9",
    2: "c4cada39-dae3-4813-9d3c-d4f02eda9b0f",
    3: "abb98eec-b4e5-469f-a9ae-b630c8546e72",
    4: "ef4da7e1-9555-4ef5-9b8f-ac0bce3d7179",
    11: "e22e0f20-fe38-4ebd-8bd8-519f9dcfab8b",
}

# Default restrictions (QloApps nao expoe via API)
# Usar endpoint manual /sync/restrictions pra override por data
DEFAULT_RESTRICTIONS = {
    "min_stay_arrival": 1,
    "stop_sell": False,
}
