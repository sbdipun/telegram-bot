import asyncio
import os
import requests
import random
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_id = int(os.getenv("api_id"))
api_hash = os.getenv("api_hash")
bot_token = os.getenv("bot_token")
YOUR_CHAT_ID = 1164918935  # Replace with your Telegram chat ID

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.respond(f"Greetings, {event.sender.first_name}! 👋 I'm your friendly bot. Let's explore what I can do. Type /help to get a list of commands.")

@client.on(events.NewMessage(pattern='/help'))
async def help_handler(event):
    help_message = """
**✨ Available Commands ✨**

* /start - Get a warm welcome.
* /help - You're already here!
* /inspire - Receive a dose of motivation.
* /joke - Tell me a funny joke. 
* /about - Learn a bit more about me.
    """
    await event.respond(help_message)


@client.on(events.NewMessage(pattern='/joke'))
async def joke_handler(event):
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    if response.status_code == 200:
        joke_data = response.json()
        if 'setup' in joke_data:  # Two-part joke
            await event.respond(joke_data['setup'])
            await asyncio.sleep(2)  # Add a slight delay for dramatic effect
            await event.respond(joke_data['punchline'])
        else:  # Single-line joke
            await event.respond(joke_data['joke'])
    else:
        await event.respond("Oops, I couldn't find a funny joke right now. Try again later.")


@client.on(events.NewMessage(pattern='/about'))
async def about_handler(event):
  await event.respond("I'm a friendly Telegram bot still learning new tricks. I'm powered by Python")


@client.on(events.NewMessage(pattern='/inspire'))
async def inspire_handler(event):
    response = requests.get("https://api.quotable.io/random")
    if response.status_code == 200:
        quote_data = response.json()
        quote = f"{quote_data['content']} - {quote_data['author']}"
        await event.respond(quote)
    else:
        await event.respond("Oops, I couldn't fetch a quote right now. Try again later.")


def main():
    """Start the bot."""
    print("\nBot started ...\n")
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
