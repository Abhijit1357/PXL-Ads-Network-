from db.db import get_publishers, get_ads, check_db_initialized
from datetime import datetime
import random
from bson import ObjectId
import traceback
import functools
import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Models")

def log_error(context, error):
    print(f"[ERROR - {context}] {error}\n{traceback.format_exc()}")

def db_required(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        from db.db import init_db
        if not check_db_initialized():
            logger.error(f"Database not initialized for {func.__name__}. Attempting to reinitialize...")
            if not await init_db():
                log_error(func.__name__, "Failed to reinitialize database.")
                return None
        return await func(*args, **kwargs)
    return wrapper

@db_required
async def register_publisher(user_id: int, username: str, bot_link: str = ""):
    try:
        logger.info(f"Registering user {user_id} with username {username}")
        data = {
            "user_id": user_id,
            "username": username,
            "bot_link": bot_link,
            "approved": False,
            "earnings": 0,
            "clicks": 0,
            "joined": datetime.utcnow()
        }
        logger.info(f"Data to insert: {data}")
        logger.info("Starting update_one operation")
        publishers = get_publishers()
        result = await asyncio.wait_for(
            publishers.update_one(
                {"user_id": user_id},
                {"$set": data},
                upsert=True
            ),
            timeout=10
        )
        logger.info(f"update_one completed: {result}")
        logger.info(f"[REGISTER] user_id={user_id} | modified={result.modified_count} | upserted={result.upserted_id}")
        logger.info("Starting find_one operation for verification")
        inserted_data = await asyncio.wait_for(
            publishers.find_one({"user_id": user_id}),
            timeout=5
        )
        logger.info(f"find_one completed: Inserted/Updated data: {inserted_data}")
        return result
    except asyncio.TimeoutError as te:
        logger.error(f"Timeout while registering user {user_id}: {te}")
        return None
    except Exception as e:
        logger.error(f"Error registering user {user_id}: {e}")
        log_error("register_publisher", e)
        return None

@db_required
async def add_bot_link(user_id: int, bot_link: str):
    try:
        publishers = get_publishers()
        await publishers.update_one(
            {"user_id": user_id},
            {"$set": {"bot_link": bot_link}}
        )
        print(f"[BOT LINK] Updated: {user_id} => {bot_link}")
    except Exception as e:
        log_error("add_bot_link", e)

@db_required
async def get_publisher(user_id: int):
    try:
        publishers = get_publishers()
        return await publishers.find_one({"user_id": user_id})
    except Exception as e:
        log_error("get_publisher", e)
        return None

get_profile = get_publisher

@db_required
async def approve_publisher(user_id: int):
    try:
        publishers = get_publishers()
        await publishers.update_one(
            {"user_id": user_id},
            {"$set": {"approved": True}}
        )
        print(f"[APPROVED] Publisher: {user_id}")
    except Exception as e:
        log_error("approve_publisher", e)

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
        ads = get_ads()
        await ads.insert_one(data)
        print(f"[SUBMIT AD] {user_id} | {ad_text}")
    except Exception as e:
        log_error("submit_ad", e)

@db_required
async def get_random_ad(exclude_owner: int = None):
    try:
        query = {"approved": True}
        if exclude_owner:
            query["owner"] = {"$ne": exclude_owner}
        ads = get_ads()
        ads_list = await ads.find(query).to_list(length=50)
        return random.choice(ads_list) if ads_list else None
    except Exception as e:
        log_error("get_random_ad", e)
        return None

@db_required
async def approve_ad(ad_id: str):
    try:
        ads = get_ads()
        await ads.update_one(
            {"_id": ObjectId(ad_id)},
            {"$set": {"approved": True}}
        )
        print(f"[APPROVE AD] id={ad_id}")
    except Exception as e:
        log_error("approve_ad", e)

@db_required
async def record_click(publisher_id: int, amount: int):
    try:
        publishers = get_publishers()
        await publishers.update_one(
            {"user_id": publisher_id},
            {"$inc": {"clicks": 1, "earnings": amount}}
        )
        print(f"[CLICK] user={publisher_id} earned={amount}")
    except Exception as e:
        log_error("record_click", e)

@db_required
async def check_eligibility(user_id: int):
    try:
        publisher = await get_publisher(user_id)
        return bool(publisher and publisher.get("approved", False))
    except Exception as e:
        log_error("check_eligibility", e)
        return False

@db_required
async def get_ad_stats(ad_id: str):
    try:
        ads = get_ads()
        return await ads.find_one({"_id": ObjectId(ad_id)})
    except Exception as e:
        log_error("get_ad_stats", e)
        return None

@db_required
async def approve_payment(publisher_id: int, amount: int):
    try:
        publishers = get_publishers()
        await publishers.update_one(
            {"user_id": publisher_id},
            {"$inc": {"earnings": amount}}
        )
        print(f"[MANUAL PAYMENT] user={publisher_id} +₹{amount}")
    except Exception as e:
        log_error("approve_payment", e)

@db_required
async def get_earnings(user_id: int):
    try:
        publisher = await get_publisher(user_id)
        return publisher.get("earnings", 0) if publisher else 0
    except Exception as e:
        log_error("get_earnings", e)
        return 0

@db_required
async def is_registered_user(user_id: int):
    try:
        logger.info(f"Checking if user {user_id} is registered")
        publishers = get_publishers()
        result = await publishers.find_one({"user_id": user_id})
        exists = result is not None
        logger.info(f"[IS REGISTERED] user={user_id} -> {exists}, result={result}")
        return exists
    except Exception as e:
        log_error("is_registered_user", e)
        return False

@db_required
async def create_profile_if_not_exists(user_id: int, username: str = ""):
    try:
        logger.info(f"Checking if profile exists for user {user_id}")
        if not await is_registered_user(user_id):
            logger.info(f"[CREATE PROFILE] New: {user_id} | {username}")
            await register_publisher(user_id, username)
        else:
            logger.info(f"[PROFILE EXISTS] user={user_id}")
    except Exception as e:
        log_error("create_profile_if_not_exists", e)

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

@db_required
async def apply_for_monetization(user_id: int):
    try:
        publishers = get_publishers()
        await publishers.update_one(
            {"user_id": user_id},
            {"$set": {"applied_for_monetization": True}}
        )
        print(f"[APPLY] user={user_id} has applied for monetization.")
    except Exception as e:
        log_error("apply_for_monetization", e)

@db_required
async def add_bot_for_approval(user_id: int, bot_username: str):
    try:
        publishers = get_publishers()
        await publishers.update_one(
            {"user_id": user_id},
            {"$set": {"bot_link": bot_username}}
        )
        print(f"[ADD BOT] user={user_id} -> {bot_username}")
    except Exception as e:
        log_error("add_bot_for_approval", e)

@db_required
async def get_user_bots(user_id: int):
    try:
        publishers = get_publishers()
        user = await publishers.find_one({"user_id": user_id})
        if user:
            return user.get("bot_link")
        return None
    except Exception as e:
        log_error("get_user_bots", e)
        return None

@db_required
async def get_stats(user_id: int):
    try:
        publishers = get_publishers()
        user = await publishers.find_one({"user_id": user_id})
        if not user:
            return None
        bots = user.get("bot_link", [])
        total_clicks = sum(bot.get("clicks", 0) for bot in bots)
        total_bots = len(bots)
        total_earnings = user.get("earnings", 0)
        return {
            "clicks": total_clicks,
            "bots": total_bots,
            "earnings": total_earnings,
        }
    except Exception as e:
        log_error("get_stats", e)
        return None
