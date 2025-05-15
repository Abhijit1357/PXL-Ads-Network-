from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

try:
    client = AsyncIOMotorClient(MONGO_URI)

    db_name = MONGO_URI.split("/")[-1].split("?")[0]
    db = client[db_name if db_name else "pxl_ads_db"]

    publishers = db["publishers"]
    ads = db["ads"]

    print("[MongoDB] Connected successfully.")
except Exception as e:
    print(f"[MongoDB] Connection Error: {e}")
    client = db = publishers = ads = None
