import asyncio
import os
import logging
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Initialize and configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

api_id = int(os.getenv("api_id"))  # Your API ID
api_hash = os.getenv("api_hash") # Your API Hash
bot_token = os.getenv("bot_token")  # Your Bot Token

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.respond(f"Greetings, {event.sender.first_name}! 👋 I'm your friendly bot. Let's explore what I can do. Type /help to get a list of commands.")

@client.on(events.NewMessage(pattern='/help'))
async def help_handler(event):
    help_message = """
**✨ Available Commands ✨**

* /start - Get a warm welcome.
* /help -  You're already here!
* /inspire -  Receive a dose of motivation.
* /joke - Tell me a funny joke. 
* /about - Learn a bit more about me.  
    """
    await event.respond(help_message)

# ... (Add handlers for other commands later: /inspire, /joke, /about) 

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
