from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI
import ssl
import certifi
import logging
from asyncio import sleep

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize global variables
client = None
db = None
publishers = None
ads = None

async def init_db():
    global client, db, publishers, ads
    
    try:
        # Create SSL context
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        
        client = AsyncIOMotorClient(
            MONGO_URI,
            tls=True,
            tlsInsecure=False,
            ssl_context=ssl_context,
            connectTimeoutMS=10000,
            serverSelectionTimeoutMS=10000
        )

        # Verify connection
        await client.admin.command('ping')
        
        # Get database name
        db_name = MONGO_URI.split("/")[-1].split("?")[0]
        db = client.get_database(db_name if db_name else "pxl_ads_db")
        
        publishers = db["publishers"]
        ads = db["ads"]
        
        logger.info("✅ MongoDB connected successfully")
        
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        await sleep(5)  # Wait before retrying
        raise

async def close_db():
    if client:
        client.close()
        logger.info("MongoDB connection closed")
