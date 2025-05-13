from db.db import publishers, ads
from datetime import datetime
import random
from bson import ObjectId

Register a new publisher
async def register_publisher(user_id: int, username: str, bot_link: str):
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

Get a publisher
async def get_publisher(user_id: int):
    return await publishers.find_one({"user_id": user_id})

Approve a publisher
async def approve_publisher(user_id: int):
    await publishers.update_one({"user_id": user_id}, {"$set": {"approved": True}})

Add a new ad
async def submit_ad(user_id: int, ad_text: str, link: str):
    data = {
        "owner": user_id,
        "text": ad_text,
        "link": link,
        "clicks": 0,
        "approved": False,
        "submitted_at": datetime.utcnow()
    }
    await ads.insert_one(data)

Get random approved ad
async def get_random_ad(exclude_owner: str = None):
    query = {"approved": True}
    if exclude_owner:
        query["owner"] = {"$ne": exclude_owner}
    ads_list = await ads.find(query).to_list(length=50)
    return random.choice(ads_list) if ads_list else None

Approve ad
async def approve_ad(ad_id):
    await ads.update_one({"_id": ObjectId(ad_id)}, {"$set": {"approved": True}})

Track clicks and earnings
async def record_click(publisher_id: int, amount: int):
    await publishers.update_one({"user_id": publisher_id}, {
        "$inc": {
            "clicks": 1,
            "earnings": amount
        }
    })

Check eligibility
async def check_eligibility(user_id: int):
    publisher = await get_publisher(user_id)
    if publisher and publisher["approved"]:
        return True
    return False

Get ad stats
async def get_ad_stats(ad_id):
    ad = await ads.find_one({"_id": ObjectId(ad_id)})
    return ad

Approve payment (example)
async def approve_payment(publisher_id, amount):
    await publishers.update_one({"user_id": publisher_id}, {"$inc": {"earnings": amount}})
