from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client["pxl_ads_db"]

publishers = db["publishers"]
ads = db["ads"]
