# ad_bot/config.py

import os

API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1001234567890"))
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "123456789").split()))

# CPM Values (example: ₹10 per 1000 impressions)
DEFAULT_CPM = float(os.getenv("DEFAULT_CPM", 10.0))

# Eligibility Settings
MIN_MEMBERS_REQUIRED = int(os.getenv("MIN_MEMBERS_REQUIRED", 100))
MIN_VIEWS_REQUIRED = int(os.getenv("MIN_VIEWS_REQUIRED", 500))
