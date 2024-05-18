#script for telegraph upload
import os
from telegraph import upload_file
import logging
from pyrogram import Client, filters
from pyrogram.types import *


# ... ( other imports and setup) ...
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('telegraph_upload')  # Create a logger
logger.setLevel(logging.DEBUG)  # Set to DEBUG for detailed logging

# Create a file handler for storing logs in a file (optional)
file_handler = logging.FileHandler('telegraph_errors.log')
file_handler.setLevel(logging.ERROR)  # Capture ERROR and above

# Add the handler to the logger
logger.addHandler(file_handler)


@Client.on_message(filters.command("tgm"))
async def telegraph_upload(bot, update):
    replied = update.reply_to_message
    if not replied:
        return await update.reply_text("𝚁𝙴𝙿𝙻𝚈 𝚃𝙾 𝙰 𝙿𝙷𝙾𝚃𝙾 𝙾𝚁 𝚅𝙸𝙳𝙴𝙾 𝚄𝙽𝙳𝙴𝚁 𝟻𝙼𝙱.")
    if not (replied.photo or replied.video):
        return await update.reply_text("please reply with valid media file")
    text = await update.reply_text("<code>Downloading to My Server ...</code>", disable_web_page_preview=True)
    media = await replied.download()
    await text.edit_text("<code>Downloading Completed. Now I am Uploading to telegra.ph Link ...</code>", disable_web_page_preview=True)
    try:
        response = upload_file(media)
    except Exception as error:
        print(error)
        return await text.edit_text(text=f"Error :- {error}", disable_web_page_preview=True)
    try:
        os.remove(media)
    except Exception as error:
        print(error)
        return
    await text.edit_text(
        text=f"<b>Link :-</b>\n\n<code>https://graph.org{response[0]}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(text="Open Link", url=f"https://graph.org{response[0]}"),
            InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url=https://graph.org{response[0]}")
            ], [
            InlineKeyboardButton(text="✗ Close ✗", callback_data="close")
            ]]
        )
    )
