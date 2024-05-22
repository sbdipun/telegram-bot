from dotenv import load_dotenv
import os
import logging
from modules.animex import get_waifu
from modules.randompass import generate_password
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.filters import regex
from modules.tele import telegraph_upload
from modules.imdbb import imdb_callback, imdb_search

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
api_id = int(os.getenv("api_id"))
api_hash = os.getenv("api_hash")
bot_token = os.getenv("bot_token")

app = Client("imdb_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Notify about bot start
async def main():
    async with app:
        # Log bot startup
        me = await app.get_me()
        logger.info(f"Bot started! Username: @{me.username}")
        await app.send_message(int(os.environ.get("OWNER_ID", "1164918935")), f"**Bot Started!!🔥**")


@app.on_message(filters.command("start"))  # Respond in both private & groups
async def start(_, message):
    logger.info(f"User {message.from_user.first_name} started the bot")
    await message.reply_text('''
    Hello {} 👋🏻
I'am A Multi use Bot with many usefull features.
Eg:- Telegarph Upload, IMDB Details etc... """'''
                             )


@app.on_message(filters.command("about"))  # Respond in both private & groups
async def about(_, message):
    await message.reply_text('''
    ╔════❰ 𝙼𝚄𝙻𝚃𝙸 𝙱𝙾𝚃 ❱═❍
║╭━━━━━━━━━━━━━━━➣
║┣⪼🤖ᴍʏ ɴᴀᴍᴇ : {bot}
║┣⪼🗣️ʟᴀɴɢᴜᴀɢᴇ : <b>https://www.python.org>ᴘʏᴛʜᴏɴ3</b>
║┣⪼📚ʟɪʙʀᴀʀʏ : <b>=https://github.com/pyrogram>ᴘʏʀᴏɢʀᴀᴍ</b> 
║┣⪼🗒️ᴠᴇʀsɪᴏɴ : 𝙼𝚄𝙻𝚃𝙸 𝙱𝙾𝚃 v1.0.0 
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍ '''
                             )


@app.on_message(filters.command("help"))
async def start(_, message):
    await message.reply_text('''
   **Available Commands**

* /start - To see if the bot is alive!
* /imdb - Fetch Movie/series Details
* /tgm - Upload image to Graph.org 
* /anime - Generates Random Anime Pics
* /pass - Generates Random Random Password
* /about - To see Bot Stats
    ''')

app.add_handler(MessageHandler(telegraph_upload, filters.command("tgm")))
app.add_handler(MessageHandler(generate_password, filters.command("pass")))
app.add_handler(MessageHandler(get_waifu, filters.command("anime")))
app.add_handler(MessageHandler(imdb_search, filters.command("imdb")))
app.add_handler(CallbackQueryHandler(imdb_callback, filters=regex(r'^imdb')))
# Start the bot

if __name__ == '__main__':
    app.run(main())
