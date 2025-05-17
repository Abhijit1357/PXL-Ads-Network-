from db.db import publishers, ads
from datetime import datetime
import random
from bson import ObjectId
from typing import Optional, Dict, Any
import traceback
from utils.logger import log_to_group

async def ensure_collections_initialized():
    """Verify collections are available before operations"""
    if publishers is None or ads is None:
        raise RuntimeError("Database collections not initialized")

async def register_publisher(user_id: int, username: str = "", bot_link: str = "") -> bool:
    """
    Register a new publisher with transaction support
    Returns True if successful, False otherwise
    """
    try:
        await ensure_collections_initialized()
        
        # Use transaction for atomic operation
        async with await client.start_session() as session:
            async with session.start_transaction():
                # Check if user exists first
                existing = await publishers.find_one(
                    {"user_id": user_id},
                    session=session
                )
                if existing:
                    return False  # Already exists
                
                # Create new profile
                result = await publishers.insert_one(
                    {
                        "user_id": user_id,
                        "username": username,
                        "bot_link": bot_link,
                        "approved": False,
                        "earnings": 0,
                        "clicks": 0,
                        "joined": datetime.utcnow()
                    },
                    session=session
                )
                return result.inserted_id is not None
                
    except Exception as e:
        error_msg = f"Publisher Registration Failed\nUser: {user_id}\nError: {str(e)}"
        print(error_msg)
        await log_to_group(error_msg)
        traceback.print_exc()
        return False

async def get_publisher(user_id: int) -> Optional[Dict[str, Any]]:
    """Get publisher data with proper error handling"""
    try:
        await ensure_collections_initialized()
        return await publishers.find_one({"user_id": user_id})
    except Exception as e:
        await log_to_group(f"⚠️ Failed to get publisher\nUser: {user_id}\nError: {str(e)}")
        return None

async def update_publisher(user_id: int, update_data: Dict[str, Any]) -> bool:
    """Generic publisher update method"""
    try:
        await ensure_collections_initialized()
        result = await publishers.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
        return result.modified_count > 0
    except Exception as e:
        await log_to_group(f"⚠️ Publisher Update Failed\nUser: {user_id}\nError: {str(e)}")
        return False

async def is_registered_user(user_id: int) -> bool:
    """Efficient check for user registration"""
    try:
        await ensure_collections_initialized()
        return await publishers.count_documents({"user_id": user_id}, limit=1) > 0
    except Exception:
        return False

async def create_profile_if_not_exists(user_id: int, username: str = "") -> bool:
    """
    Enhanced profile creation with verification
    Returns:
        True: if profile was created
        False: if profile already exists or creation failed
    """
    try:
        # First verify registration status
        if await is_registered_user(user_id):
            return False
            
        # Attempt creation
        created = await register_publisher(user_id, username)
        if not created:
            return False
            
        # Verify creation was successful
        return await is_registered_user(user_id)
        
    except Exception as e:
        error_msg = f"Profile Creation Failed\nUser: {user_id}\nError: {str(e)}"
        print(error_msg)
        await log_to_group(error_msg)
        return False

async def get_profile_data(user_id: int) -> Dict[str, Any]:
    """Structured profile data with defaults"""
    publisher = await get_publisher(user_id)
    if not publisher:
        return {}
    
    return {
        "earnings": publisher.get("earnings", 0),
        "clicks": publisher.get("clicks", 0),
        "approved": publisher.get("approved", False),
        "bot_link": publisher.get("bot_link", ""),
        "username": publisher.get("username", "")
    }

# Ad-related operations
async def submit_ad(user_id: int, ad_text: str, link: str) -> Optional[ObjectId]:
    """Submit new ad and return its ID"""
    try:
        await ensure_collections_initialized()
        ad_data = {
            "owner": user_id,
            "text": ad_text,
            "link": link,
            "clicks": 0,
            "approved": False,
            "submitted_at": datetime.utcnow()
        }
        result = await ads.insert_one(ad_data)
        return result.inserted_id
    except Exception as e:
        await log_to_group(f"⚠️ Ad Submission Failed\nUser: {user_id}\nError: {str(e)}")
        return None

async def get_ad_stats(ad_id: str) -> Optional[Dict[str, Any]]:
    """Get advertisement statistics by ID"""
    try:
        await ensure_collections_initialized()
        return await ads.find_one({"_id": ObjectId(ad_id)})
    except Exception as e:
        await log_to_group(f"⚠️ Failed to get ad stats\nAd ID: {ad_id}\nError: {str(e)}")
        return None

async def get_random_ad(exclude_owner: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """Get random approved ad with optional owner exclusion"""
    try:
        await ensure_collections_initialized()
        pipeline = [{"$match": {"approved": True}}]
        
        if exclude_owner:
            pipeline.append({"$match": {"owner": {"$ne": exclude_owner}}})
        
        pipeline.append({"$sample": {"size": 1}})
        
        cursor = ads.aggregate(pipeline)
        result = await cursor.to_list(length=1)
        return result[0] if result else None
    except Exception as e:
        await log_to_group(f"⚠️ Failed to get random ad\nError: {str(e)}")
        return None

# Economic operations
async def record_click(publisher_id: int, amount: int) -> bool:
    """Record click and update earnings atomically"""
    try:
        await ensure_collections_initialized()
        result = await publishers.update_one(
            {"user_id": publisher_id},
            {
                "$inc": {
                    "clicks": 1,
                    "earnings": amount
                }
            }
        )
        return result.modified_count > 0
    except Exception as e:
        await log_to_group(f"⚠️ Click Recording Failed\nUser: {publisher_id}\nError: {str(e)}")
        return False

async def get_earnings(user_id: int) -> float:
    """Get current earnings for a publisher"""
    try:
        await ensure_collections_initialized()
        publisher = await publishers.find_one({"user_id": user_id})
        return float(publisher.get("earnings", 0)) if publisher else 0.0
    except Exception as e:
        await log_to_group(f"⚠️ Failed to get earnings\nUser: {user_id}\nError: {str(e)}")
        return 0.0

# Admin operations
async def approve_publisher(user_id: int) -> bool:
    """Approve publisher account"""
    return await update_publisher(user_id, {"approved": True})

async def approve_ad(ad_id: str) -> bool:
    """Approve specific ad"""
    try:
        await ensure_collections_initialized()
        result = await ads.update_one(
            {"_id": ObjectId(ad_id)},
            {"$set": {"approved": True}}
        )
        return result.modified_count > 0
    except Exception as e:
        await log_to_group(f"⚠️ Ad Approval Failed\nAd: {ad_id}\nError: {str(e)}")
        return False

async def approve_payment(publisher_id: int, amount: int) -> bool:
    """Manually approve payment for publisher"""
    try:
        await ensure_collections_initialized()
        result = await publishers.update_one(
            {"user_id": publisher_id},
            {"$inc": {"earnings": amount}}
        )
        return result.modified_count > 0
    except Exception as e:
        await log_to_group(f"⚠️ Payment Approval Failed\nUser: {publisher_id}\nError: {str(e)}")
        return False
