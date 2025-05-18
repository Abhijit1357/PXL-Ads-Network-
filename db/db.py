# db/db.py

from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI
import certifi
import logging
from asyncio import sleep

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("MongoDB")

# Initialize connection variables
client = None
db = None
publishers = None
ads = None
db_initialized = False

async def init_db():
    """Initialize MongoDB connection with retry and TLS"""
    global client, db, publishers, ads, db_initialized
    max_retries = 5
    retry_delay = 3  # seconds between retries

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

            # Check connection
            await client.admin.command('ping')

            # Extract database name from URI or default
            db_name = MONGO_URI.split("/")[-1].split("?")[0] or "pxl_ads_db"
            db = client[db_name]

            # Create collections if they don't exist
            if 'publishers' not in await db.list_collection_names():
                await db.create_collection('publishers')
            if 'ads' not in await db.list_collection_names():
                await db.create_collection('ads')

            # Get collections
            publishers = db['publishers']
            ads = db['ads']

            # Create indexes
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
    """Close the MongoDB connection cleanly"""
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
    """Ensure database is initialized before performing operations"""
    if not db_initialized or None in (client, db, publishers, ads):
        logger.error("❗ Database not initialized or disconnected.")
        return False
    return True
