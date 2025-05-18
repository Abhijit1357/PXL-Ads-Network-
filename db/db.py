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
                connectTimeoutMS=10000,
                serverSelectionTimeoutMS=10000,
                retryWrites=True,
                retryReads=True,
                socketTimeoutMS=5000,
                maxPoolSize=20,
                maxIdleTimeMS=5000,
                heartbeatFrequencyMS=5000
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
            # Drop and recreate index
            try:
                await publishers.drop_index("user_id_1")
                logger.info("Dropped existing user_id index")
            except Exception as e:
                logger.info(f"No user_id index to drop: {e}")
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
    global client, db, publishers, ads, db_initialized
    if client:
        try:
            client.close()
            logger.info("🛑 MongoDB connection closed.")
        except Exception as e:
            logger.error(f"Error while closing MongoDB: {e}")
    # Reset variables
    client = None
    db = None
    publishers = None
    ads = None
    db_initialized = False

def check_db_initialized():
    global publishers, ads, db_initialized
    if not db_initialized or publishers is None or ads is None:
        logger.error(f"❗ Database not initialized or disconnected. db_initialized={db_initialized}, publishers={publishers}, ads={ads}")
        return False
    logger.info("✅ Database initialized and ready")
    return True
