# Generates random images from a free api website waifu
import random
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging

# Configure the logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO  # You can adjust the logging level as needed
)
logger = logging.getLogger(__name__)

# Regex for photos
regex_photo = ["waifu", "neko", "pat", "bunk", "smug", "happy"]


@Client.on_message(filters.command("anime"))
async def get_waifu(_, message):
    try:  
        pht = random.choice(regex_photo)
        url = f"https://api.waifu.pics/sfw/{pht}"
        logger.info(f"Requesting image from API for type: {pht}")  # Log the request type
        text = await message.reply_text("<code>Generating....", disable_web_page_preview=True)
        logger.info(f"Generating...")
        await text.edit_text(f"Generated!!")
        await text.delete()

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            up = data['url']
            if up:
                button = [[InlineKeyboardButton("Owner 🌺", url=f't.me/kingsb007')]]
                markup = InlineKeyboardMarkup(button)
                await message.reply_photo(up, caption="**Mutli Usage Bot**", reply_markup=markup)
                logger.info(f"Successfully sent image: {up}")  # Log successful image send
            else:
                logger.warning("No image URL found in API response")  # Log warning
                await message.reply_text("Request failed, try again")
        else:
            logger.error(f"API request failed with status code: {response.status_code}")  # Log the error
            await message.reply_text("Request failed, try again")
    except Exception as e:
        logger.exception(f"Error in get_waifu: {e}")  # Log the exception with traceback
        await message.reply_text("An unexpected error occurred.")
