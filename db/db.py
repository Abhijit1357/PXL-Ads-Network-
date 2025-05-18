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
    logger.info(f"MONGO_URI: {MONGO_URI}")
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting MongoDB connection {attempt+1}/{max_retries}")
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
            logger.info("Ping successful")
            db_name = MONGO_URI.split("/")[-1].split("?")[0] or "pxl_ads_db"
            logger.info(f"Using database: {db_name}")
            db = client[db_name]
            collections = await db.list_collection_names()
            logger.info(f"Existing collections: {collections}")
            if 'publishers' not in collections:
                await db.create_collection('publishers')
                logger.info("Created publishers collection")
            if 'ads' not in collections:
                await db.create_collection('ads')
                logger.info("Created ads collection")
            publishers = db['publishers']
            ads = db['ads']
            logger.info(f"Publishers collection set: {publishers}")
            logger.info(f"Ads collection set: {ads}")
            await publishers.create_index("user_id", unique=True)
            await ads.create_index("owner")
            await ads.create_index("approved")
            logger.info("✅ MongoDB connected and initialized.")
            db_initialized = True
            return True
        except Exception as e:
            logger.error(f"❌ Attempt {attempt+1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                await sleep(retry_delay)
            else:
                logger.error("❌ All connection attempts failed.")
                return False
    logger.error("❌ Failed to initialize DB after all retries")
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
        logger.error(f"❗ Database not initialized or disconnected. client={client}, db={db}, publishers={publishers}, ads={ads}")
        return False
    logger.info("✅ Database initialized and ready")
    return True
