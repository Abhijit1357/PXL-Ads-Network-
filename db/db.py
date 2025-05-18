from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI
import certifi
import logging
from asyncio import sleep

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("MongoDB")

client = None
db = None
publishers = None
ads = None
db_initialized = False

async def init_db():
    global client, db, publishers, ads, db_initialized
    max_retries = 5
    retry_delay = 3  
    for attempt in range(max_retries):
        try:
            client = AsyncIOMotorClient(
                MONGO_URI,
                tls=True,
                tlsCAFile=certifi.where(),
                connectTimeoutMS=15000,
                serverSelectionTimeoutMS=15000,
                retryWrites=True,
                retryReads=True,
                socketTimeoutMS=30000
            )
            await client.admin.command('ping')
            db_name = MONGO_URI.split("/")[-1].split("?")[0] or "pxl_ads_db"
            db = client[db_name]
            if 'publishers' not in await db.list_collection_names():
                await db.create_collection('publishers')
            if 'ads' not in await db.list_collection_names():
                await db.create_collection('ads')
            publishers = db['publishers']
            ads = db['ads']
            await publishers.create_index("user_id", unique=True)
            await ads.create_index("owner")
            await ads.create_index("approved")
            logger.info("✅ MongoDB connected and initialized.")
            db_initialized = True
            return True
        except Exception as e:
            logger.error(f"❌ MongoDB connection attempt {attempt+1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                await sleep(retry_delay)
            else:
                logger.error("❌ All connection attempts failed.")
                return False

async def close_db():
    global client, db_initialized, db, publishers, ads
    if client:
        try:
            client.close()
            logger.info("🛑 MongoDB connection closed.")
        except Exception as e:
            logger.error(f"Error while closing MongoDB: {e}")
        finally:
            client = None
            db = None
            publishers = None
            ads = None
            db_initialized = False

def check_db_initialized():
    if not db_initialized or None in (client, db, publishers, ads):
        logger.error("❗ Database not initialized or disconnected.")
        return False
    return True
