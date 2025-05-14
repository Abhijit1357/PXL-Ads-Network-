from db.db import publishers, ads
from datetime import datetime
import random
from bson import ObjectId

#Register a new publisher
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
        print(f"Error: {e}")

#Get a publisher
async def get_publisher(user_id: int):
    try:
        return await publishers.find_one({"user_id": user_id})
    except Exception as e:
        print(f"Error: {e}")
        return None

#Approve a publisher
async def approve_publisher(user_id: int):
    try:
        await publishers.update_one({"user_id": user_id}, {"$set": {"approved": True}})
    except Exception as e:
        print(f"Error: {e}")

#Add a new ad
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
        print(f"Error: {e}")

#Get random approved ad
async def get_random_ad(exclude_owner: str = None):
    try:
        query = {"approved": True}
        if exclude_owner:
            query["owner"] = {"$ne": exclude_owner}
        ads_list = await ads.find(query).to_list(length=50)
        return random.choice(ads_list) if ads_list else None
    except Exception as e:
        print(f"Error: {e}")
        return None

#Approve ad
async def approve_ad(ad_id):
    try:
        await ads.update_one({"_id": ObjectId(ad_id)}, {"$set": {"approved": True}})
    except Exception as e:
        print(f"Error: {e}")

#Track clicks and earnings
async def record_click(publisher_id: int, amount: int):
    try:
        await publishers.update_one({"user_id": publisher_id}, {"$inc": {"clicks": 1, "earnings": amount}})
    except Exception as e:
        print(f"Error: {e}")

#Check eligibility
async def check_eligibility(user_id: int):
    try:
        publisher = await get_publisher(user_id)
        if publisher and publisher["approved"]:
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

#Get ad stats
async def get_ad_stats(ad_id):
    try:
        ad = await ads.find_one({"_id": ObjectId(ad_id)})
        return ad
    except Exception as e:
        print(f"Error: {e}")
        return None

#Approve payment (example)
async def approve_payment(publisher_id, amount):
    try:
        await publishers.update_one({"user_id": publisher_id}, {"$inc": {"earnings": amount}})
    except Exception as e:
        print(f"Error: {e}")

##Get earnings
async def get_earnings(user_id: int):
    try:
        publisher = await publishers.find_one({"user_id": user_id})
        if publisher:
            return publisher.get("earnings", 0)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return None

#Is registered user
async def is_registered_user(user_id: int):
    try:
        publisher = await publishers.find_one({"user_id": user_id})
        return publisher is not None
    except Exception as e:
        print(f"Error: {e}")
        return False

#Create profile if not exists
async def create_profile_if_not_exists(user_id: int, username: str = "", bot_link: str = ""):
    try:
        publisher = await publishers.find_one({"user_id": user_id})
        if not publisher:
            await register_publisher(user_id, username, bot_link)
    except Exception as e:
        print(f"Error: {e}")

#Get profile data
async def get_profile_data(user_id: int):
    try:
        publisher = await publishers.find_one({"user_id": user_id})
        if publisher:
            return {
                "earnings": publisher.get("earnings", 0),
                # Add other fields as needed
            }
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
