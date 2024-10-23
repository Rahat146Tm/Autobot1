from pymongo import MongoClient
from datetime import datetime
import os

# MongoDB connection
mongo_client = MongoClient(os.environ.get("MONGO_URL"))
db = mongo_client["movie_bot_db"]
user_collection = db["users"]

# Profile management functions
def create_profile(user_id, name):
    user_collection.insert_one({"user_id": user_id, "name": name, "watchlist": [], "downloads": 0})

def update_profile(user_id, field, value):
    user_collection.update_one({"user_id": user_id}, {"$set": {field: value}})

# Watchlist management functions
def add_to_watchlist(user_id, movie_name
