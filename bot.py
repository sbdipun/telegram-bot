import asyncio
import os
import dotenv
import json, logging,asyncio, requests
import logging
from telethon import TelegramClient, events
from modules import text, info
from dotenv import load_dotenv
loadenv()

# Initialize and configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

api_id = int(os.getenv("api_id"))  # Your API ID
api_hash = ("api_hash") # Your API Hash
bot_token = ("bot_token")  # Your Bot Token

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Registering handlers from the handlers package
client.add_event_handler(info.info_handler)
client.add_event_handler(text.text_handler)

async def main():
    # Log on startup instead of printing to the console
    logger.info("Bot has started!")
    
    try:
        # Run the client until, or the client disconnects
        await client.run_until_disconnected()
    except Exception as e:
        logger.exception("An unexpected error occurred: %s", e)
    finally:
        # Optional: perform cleanup here if needed when the bot is stopped
        logger.info("Bot has stopped!")

if __name__ == '__main__':
    asyncio.run(main())
