from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

try:
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.get_default_database() or client["pxl_ads_db"]

    # Collections
    publishers = db["publishers"]
    ads = db["ads"]

    print("[MongoDB] Connected successfully.")
except Exception as e:
    print(f"[MongoDB] Connection Error: {e}")
    client = None
    db = None
    publishers = None
    ads = None
