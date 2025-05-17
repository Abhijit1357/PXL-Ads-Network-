from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI
import certifi
import logging
from asyncio import sleep

#Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

#Initialize connection variables
client = None
db = None
publishers = None
ads = None
db_initialized = False

async def init_db():
    """Initialize database connection with retry logic"""
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
            # Verify connection
            await client.admin.command('ping')
            # Get database
            db_name = MONGO_URI.split("/")[-1].split("?")[0]
            db = client.get_database(db_name if db_name else "pxl_ads_db")
            # Initialize collections with validation
            if 'publishers' not in await db.list_collection_names():
                await db.create_collection('publishers')
            if 'ads' not in await db.list_collection_names():
                await db.create_collection('ads')
            publishers = db['publishers']
            ads = db['ads']
            # Create indexes
            await publishers.create_index([("user_id", 1)], unique=True)
            await ads.create_index([("owner", 1)])
            await ads.create_index([("approved", 1)])
            logger.info("✅ MongoDB connected successfully")
            db_initialized = True
            return True
        except Exception as e:
            logger.error(f"❌ Connection attempt {attempt+1}/{max_retries} failed: {str(e)}")
            if attempt < max_retries - 1:
                await sleep(retry_delay)
                continue
            logger.error("❌ Failed to connect to MongoDB after retries")
            return False

async def close_db():
    """Properly close database connection"""
    global client, db_initialized
    if client:
        try:
            client.close()
            logger.info("MongoDB connection closed")
        except Exception as e:
            logger.error(f"Error closing connection: {str(e)}")
        finally:
            client = None
            db = None
            publishers = None
            ads = None
            db_initialized = False

def check_db_initialized():
    """Verify database is ready for operations"""
    if not db_initialized or None in [client, db, publishers, ads]:
        logger.error("Database not properly initialized")
        return False
    return True
