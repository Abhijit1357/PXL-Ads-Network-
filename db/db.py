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
logger = logging.getLogger(__name__)

# Initialize connection variables
client = None
db = None
publishers = None
ads = None
db_initialized = False  # Track initialization status

async def init_db():
    """Initialize database connection with retry logic"""
    global client, db, publishers, ads, db_initialized
    
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            client = AsyncIOMotorClient(
                MONGO_URI,
                tls=True,
                tlsCAFile=certifi.where(),
                connectTimeoutMS=10000,
                serverSelectionTimeoutMS=10000,
                retryWrites=True,
                retryReads=True
            )
            
            # Verify connection
            await client.admin.command('ping')
            
            # Get database name
            db_name = MONGO_URI.split("/")[-1].split("?")[0]
            db = client.get_database(db_name if db_name else "pxl_ads_db")
            
            # Initialize collections
            publishers = db["publishers"]
            ads = db["ads"]
            
            # Create indexes
            await publishers.create_index("user_id", unique=True)
            await ads.create_index("owner")
            await ads.create_index("approved")
            
            logger.info("✅ MongoDB connected successfully")
            db_initialized = True
            return True
            
        except Exception as e:
            logger.error(f"❌ MongoDB connection failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                await sleep(retry_delay)
                continue
            db_initialized = False
            raise

async def close_db():
    """Close database connection"""
    global client, db_initialized
    if client:
        try:
            client.close()
            logger.info("MongoDB connection closed")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {e}")
        finally:
            client = None
            db = None
            publishers = None
            ads = None
            db_initialized = False

def check_db_initialized():
    """Check if database is properly initialized"""
    if not db_initialized:
        logger.error("Database not initialized! Call init_db() first")
        return False
    if None in [client, db, publishers, ads]:
        logger.error("Database components not properly initialized")
        return False
    return True
