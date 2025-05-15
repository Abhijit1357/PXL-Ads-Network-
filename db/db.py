from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI
import ssl
import certifi
from urllib.parse import quote_plus
from aiogram.utils.exceptions import RetryAfter
import logging

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
        # Create SSL context for secure connection
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        
        # Configure client with timeout and retry options
        client = AsyncIOMotorClient(
            MONGO_URI,
            tls=True,
            tlsInsecure=False,
            tlsAllowInvalidCertificates=False,
            ssl_cert_reqs=ssl.CERT_REQUIRED,
            ssl_context=ssl_context,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000,
            serverSelectionTimeoutMS=10000,
            retryWrites=True,
            retryReads=True,
            maxPoolSize=100,
            minPoolSize=10
        )

        # Verify connection
        await client.admin.command('ping')
        
        # Get database name from URI or use default
        db_name = MONGO_URI.split("/")[-1].split("?")[0]
        db = client.get_database(db_name if db_name else "pxl_ads_db")
        
        # Initialize collections
        publishers = db["publishers"]
        ads = db["ads"]
        
        # Create indexes if they don't exist
        await publishers.create_index("user_id", unique=True)
        await ads.create_index("owner")
        await ads.create_index("approved")
        
        logger.info("[MongoDB] Connected successfully with indexes created.")
        
    except Exception as e:
        logger.error(f"[MongoDB] Connection Error: {str(e)}")
        # Implement retry logic or graceful degradation
        raise RetryAfter(5)  # Wait 5 seconds before retrying

async def close_db():
    global client
    if client:
        client.close()
        logger.info("[MongoDB] Connection closed gracefully.")

# Helper function for safe ObjectId conversion
def to_objectid(id_str):
    from bson import ObjectId
    try:
        return ObjectId(id_str)
    except:
        return None
