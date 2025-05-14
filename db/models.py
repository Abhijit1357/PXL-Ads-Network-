from db.db import publishers, ads
from datetime import datetime
import random
from bson import ObjectId
import traceback

# Utility for error logging
def log_error(context, error):
    print(f"[Error - {context}] {error}")
    print(traceback.format_exc())

# Register a new publisher
async def register_publisher(user_id: int, username: str, bot_link: str):
    try:
        data = {
            "user_id": user_id,
            "username": username,
            "bot_link": bot_link,
            "approved": False,
            "earnings": 0,
            "clicks": 0,
            "joined": datetime.utcnow()
        }
        await publishers.update_one({"user_id": user_id}, {"$set": data}, upsert=True)
    except Exception as e:
        log_error("register_publisher", e)

# Get a publisher
async def get_publisher(user_id: int):
    try:
        return await publishers.find_one({"user_id": user_id})
    except Exception as e:
        log_error("get_publisher", e)
        return None

# Approve a publisher
async def approve_publisher(user_id: int):
    try:
        await publishers.update_one({"user_id": user_id}, {"$set": {"approved": True}})
    except Exception as e:
        log_error("approve_publisher", e)

# Submit a new ad
async def submit_ad(user_id: int, ad_text: str, link: str):
    try:
        data = {
            "owner": user_id,
            "text": ad_text,
            "link": link,
            "clicks": 0,
            "approved": False,
            "submitted_at": datetime.utcnow()
        }
        await ads.insert_one(data)
    except Exception as e:
        log_error("submit_ad", e)

# Get random approved ad
async def get_random_ad(exclude_owner: int = None):
    try:
        query = {"approved": True}
        if exclude_owner:
            query["owner"] = {"$ne": exclude_owner}
        ads_list = await ads.find(query).to_list(length=50)
        return random.choice(ads_list) if ads_list else None
    except Exception as e:
        log_error("get_random_ad", e)
        return None

# Approve ad
async def approve_ad(ad_id: str):
    try:
        await ads.update_one({"_id": ObjectId(ad_id)}, {"$set": {"approved": True}})
    except Exception as e:
        log_error("approve_ad", e)

# Record click and update earnings
async def record_click(publisher_id: int, amount: int):
    try:
        await publishers.update_one(
            {"user_id": publisher_id},
            {"$inc": {"clicks": 1, "earnings": amount}}
        )
    except Exception as e:
        log_error("record_click", e)

# Check if user is approved publisher
async def check_eligibility(user_id: int):
    try:
        publisher = await get_publisher(user_id)
        return bool(publisher and publisher.get("approved", False))
    except Exception as e:
        log_error("check_eligibility", e)
        return False

# Get ad stats by ID
async def get_ad_stats(ad_id: str):
    try:
        return await ads.find_one({"_id": ObjectId(ad_id)})
    except Exception as e:
        log_error("get_ad_stats", e)
        return None

# Approve payment manually
async def approve_payment(publisher_id: int, amount: int):
    try:
        await publishers.update_one({"user_id": publisher_id}, {"$inc": {"earnings": amount}})
    except Exception as e:
        log_error("approve_payment", e)

# Get publisher earnings
async def get_earnings(user_id: int):
    try:
        publisher = await publishers.find_one({"user_id": user_id})
        return publisher.get("earnings", 0) if publisher else 0
    except Exception as e:
        log_error("get_earnings", e)
        return 0

# Check if user is registered
async def is_registered_user(user_id: int):
    try:
        return await publishers.find_one({"user_id": user_id}) is not None
    except Exception as e:
        log_error("is_registered_user", e)
        return False

# Create profile if it doesn't exist
async def create_profile_if_not_exists(user_id: int, username: str = "", bot_link: str = ""):
    try:
        if not await is_registered_user(user_id):
            await register_publisher(user_id, username, bot_link)
    except Exception as e:
        log_error("create_profile_if_not_exists", e)

# Get profile data
async def get_profile_data(user_id: int):
    try:
        publisher = await get_publisher(user_id)
        if publisher:
            return {
                "earnings": publisher.get("earnings", 0),
                "clicks": publisher.get("clicks", 0),
                "approved": publisher.get("approved", False),
                "bot_link": publisher.get("bot_link", "")
            }
        return None
    except Exception as e:
        log_error("get_profile_data", e)
        return None
