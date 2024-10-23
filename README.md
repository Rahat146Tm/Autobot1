# Movie Auto Filter Bot

This Telegram bot allows users to search for movies, provide feedback, and manage a movie database with advanced features.

## New Features

- **Multi-Channel Force Subscription**: Users must join multiple channels before using the bot.
- **Automatic Database Backup**: The MongoDB database is automatically backed up every day.
- **Movie Feedback System**: Users can provide feedback and ratings on movies.
- **Spam Detection System**: Detects and prevents spam messages.
- **Movie Poster Sharing**: Movies are shared with posters for better presentation.

## Setup

1. Clone the repository.
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up environment variables:
    - `API_ID`, `API_HASH`, `BOT_TOKEN`, `MONGO_URL`, `OWNER_ID`, `FORCE_SUB_CHANNELS`
4. Run the bot:
    ```bash
    python main.py
    ```

## License

This project is licensed under the MIT License.
