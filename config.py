import os

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/")
IMDB_API_KEY = os.environ.get("IMDB_API_KEY")
OWNER_ID = int(os.environ.get("OWNER_ID"))
PORT = int(os.environ.get("PORT", 5000))
FORCE_SUB_CHANNELS = os.environ.get("FORCE_SUB_CHANNELS")  # Multiple channels, comma-separated
LANGUAGES = ["English", "Bengali", "Spanish"]  # Add more languages as needed
DOWNLOAD_LIMIT = int(os.environ.get("DOWNLOAD_LIMIT", 5))  # Daily download limit per user
