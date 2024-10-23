import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from imdb_template import get_movie_info
import logging
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URL, OWNER_ID, PORT, FORCE_SUB_CHANNELS, LANGUAGES
from utils import generate_movie_buttons, is_admin, send_backup_to_cloud, get_user_language, set_user_language
from flask import Flask
import schedule

# MongoDB Connection
mongo_client = MongoClient(MONGO_URL)
db = mongo_client["movie_bot_db"]
movie_collection = db["movies"]

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize the bot
bot = Client("movie_auto_filter_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Flask app for health check
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running"

# Force Subscription Check for multiple channels
async def force_subscribe(client, message):
    for channel in FORCE_SUB_CHANNELS.split(","):
        try:
            user_status = await client.get_chat_member(channel.strip(), message.from_user.id)
            if user_status.status == 'kicked':
                await message.reply_text("You have been banned from one of our channels.")
                return False
        except:
            buttons = [[InlineKeyboardButton("Join Channels", url=f"https://t.me/{channel.strip()}")]]
            await message.reply_text(f"You need to join all the channels to use the bot.", reply_markup=InlineKeyboardMarkup(buttons))
            return False
    return True

# Multi-language Support
@bot.on_message(filters.command("language") & filters.private)
async def change_language(client, message):
    lang_buttons = [[InlineKeyboardButton(f"{lang}", callback_data=f"set_lang_{lang}") for lang in LANGUAGES]]
    await message.reply_text("Please select your language:", reply_markup=InlineKeyboardMarkup(lang_buttons))

@bot.on_callback_query(filters.regex(r"set_lang_(.*)"))
async def set_language(client, callback_query):
    selected_lang = callback_query.data.split("_")[2]
    set_user_language(callback_query.from_user.id, selected_lang)
    await callback_query.answer(f"Language set to {selected_lang}", show_alert=True)

# Auto-delete after certain time
@bot.on_message(filters.command("add_movie") & filters.private)
async def add_movie(client, message):
    if not (await is_admin(client, message) or message.from_user.id == OWNER_ID):
        await message.reply_text("You don't have permission to use this command.")
        return

    if len(message.command) < 3:
        await message.reply_text("Usage: /add_movie <movie_name> <link>")
        return

    movie_name = message.command[1]
    movie_link = message.command[2]
    movie_collection.insert_one({"name": movie_name, "link": movie_link})
    await message.reply_text(f"Movie '{movie_name}' added successfully!")

    # Auto-delete message after 24 hours
    await asyncio.sleep(86400)
    await message.delete()

# Movie Top Rated List
@bot.on_message(filters.command("top_rated") & filters.private)
async def top_rated_movies(client, message):
    top_movies = movie_collection.find().sort([("rating", -1)]).limit(10)
    response = "Top 10 Rated Movies:\n\n"
    for movie in top_movies:
        response += f"{movie['name']} - {movie['rating']}⭐\n"
    await message.reply_text(response)

# Bulk Movie Uploading
@bot.on_message(filters.command("bulk_upload") & filters.private)
async def bulk_upload(client, message):
    if not (await is_admin(client, message) or message.from_user.id == OWNER_ID):
        await message.reply_text("You don't have permission to use this command.")
        return

    if len(message.command) < 2:
        await message.reply_text("Usage: /bulk_upload <movie_links>")
        return

    movie_links = message.text.split("\n")[1:]
    for movie_link in movie_links:
        movie_name, link = movie_link.split(" - ")
        movie_collection.insert_one({"name": movie_name, "link": link})
    await message.reply_text(f"Bulk movie upload successful!")

# Run the bot and Flask app for health check
if __name__ == "__main__":
    asyncio.get_event_loop().create_task(bot.start())
    app.run(host="0.0.0.0", port=PORT)
