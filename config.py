# ad_bot/config.py

import os

API_ID = int(os.getenv("API_ID", "22834593"))
API_HASH = os.getenv("API_HASH", "f400bc1d1baeb9ae93014ce3ee5ea835")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7386024380:AAEDZ5HvvQA1XrK_RILlHVrDoTvQNJXRYAw")
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://AOMusic:AOMusic@cluster0.sibxiqk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002134425165"))
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "6148346742").split()))

# CPM Values (example: ₹10 per 1000 impressions)
DEFAULT_CPM = float(os.getenv("DEFAULT_CPM", 10.0))

# Eligibility Settings
MIN_MEMBERS_REQUIRED = int(os.getenv("MIN_MEMBERS_REQUIRED", 100))
MIN_VIEWS_REQUIRED = int(os.getenv("MIN_VIEWS_REQUIRED", 500))
