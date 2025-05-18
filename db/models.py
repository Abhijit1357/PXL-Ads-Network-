from db.db import publishers, ads, check_db_initialized
from datetime import datetime
import random
from bson import ObjectId
import traceback
import functools
import asyncio

# Utility for error logging
def log_error(context, error):
    print(f"[ERROR - {context}] {error}\n{traceback.format_exc()}")

# Decorator to check DB initialization before running the function
def db_required(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if not check_db_initialized():
            log_error(func.__name__, "Database not initialized.")
            return None
        return await func(*args, **kwargs)
    return wrapper

# Register a new publisher
@db_required
async def register_publisher(user_id: int, username: str, bot_link: str = ""):
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
        result = await publishers.update_one(
            {"user_id": user_id},
            {"$set": data},
            upsert=True
        )
        print(f"[REGISTER] user_id={user_id} | modified={result.modified_count} | upserted={result.upserted_id}")
        return result
    except Exception as e:
        log_error("register_publisher", e)
        return None

# Add or update bot link
@db_required
async def add_bot_link(user_id: int, bot_link: str):
    try:
        await publishers.update_one(
            {"user_id": user_id},
            {"$set": {"bot_link": bot_link}}
        )
        print(f"[BOT LINK] Updated: {user_id} => {bot_link}")
    except Exception as e:
        log_error("add_bot_link", e)

# Get a publisher
@db_required
async def get_publisher(user_id: int):
    try:
        return await publishers.find_one({"user_id": user_id})
    except Exception as e:
        log_error("get_publisher", e)
        return None

# Alias
get_profile = get_publisher

# Approve a publisher
@db_required
async def approve_publisher(user_id: int):
    try:
        await publishers.update_one(
            {"user_id": user_id},
            {"$set": {"approved": True}}
        )
        print(f"[APPROVED] Publisher: {user_id}")
    except Exception as e:
        log_error("approve_publisher", e)

# Submit ad
@db_required
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
        print(f"[SUBMIT AD] {user_id} | {ad_text}")
    except Exception as e:
        log_error("submit_ad", e)

# Get random approved ad
@db_required
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
@db_required
async def approve_ad(ad_id: str):
    try:
        await ads.update_one(
            {"_id": ObjectId(ad_id)},
            {"$set": {"approved": True}}
        )
        print(f"[APPROVE AD] id={ad_id}")
    except Exception as e:
        log_error("approve_ad", e)

# Record click and earnings
@db_required
async def record_click(publisher_id: int, amount: int):
    try:
        await publishers.update_one(
            {"user_id": publisher_id},
            {"$inc": {"clicks": 1, "earnings": amount}}
        )
        print(f"[CLICK] user={publisher_id} earned={amount}")
    except Exception as e:
        log_error("record_click", e)

# Check if approved
@db_required
async def check_eligibility(user_id: int):
    try:
        publisher = await get_publisher(user_id)
        return bool(publisher and publisher.get("approved", False))
    except Exception as e:
        log_error("check_eligibility", e)
        return False

# Ad stats by ID
@db_required
async def get_ad_stats(ad_id: str):
    try:
        return await ads.find_one({"_id": ObjectId(ad_id)})
    except Exception as e:
        log_error("get_ad_stats", e)
        return None

# Manual earnings add
@db_required
async def approve_payment(publisher_id: int, amount: int):
    try:
        await publishers.update_one(
            {"user_id": publisher_id},
            {"$inc": {"earnings": amount}}
        )
        print(f"[MANUAL PAYMENT] user={publisher_id} +₹{amount}")
    except Exception as e:
        log_error("approve_payment", e)

# Get earnings only
@db_required
async def get_earnings(user_id: int):
    try:
        publisher = await get_publisher(user_id)
        return publisher.get("earnings", 0) if publisher else 0
    except Exception as e:
        log_error("get_earnings", e)
        return 0

# Check if registered
@db_required
async def is_registered_user(user_id: int):
    try:
        exists = await publishers.find_one({"user_id": user_id}) is not None
        print(f"[IS REGISTERED] user={user_id} -> {exists}")
        return exists
    except Exception as e:
        log_error("is_registered_user", e)
        return False

# Create if not exists
@db_required
async def create_profile_if_not_exists(user_id: int, username: str = ""):
    try:
        if not await is_registered_user(user_id):
            print(f"[CREATE PROFILE] New: {user_id} | {username}")
            await register_publisher(user_id, username)
        else:
            print(f"[PROFILE EXISTS] user={user_id}")
    except Exception as e:
        log_error("create_profile_if_not_exists", e)

# Profile summary
@db_required
async def get_profile_data(user_id: int):
    try:
        print(f"Getting profile data for user {user_id}")  
        publisher = await get_publisher(user_id)
        print(f"Publisher data: {publisher}")  
        if publisher:
            return {
                "earnings": publisher.get("earnings", 0),
                "clicks": publisher.get("clicks", 0),
                "approved": publisher.get("approved", False),
                "bot_link": publisher.get("bot_link", "")
            }
        print("Publisher not found")  
        return None
    except Exception as e:
        log_error("get_profile_data", e)
        print(f"Error: {e}")  
        return None
