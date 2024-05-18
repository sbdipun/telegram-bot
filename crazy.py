from dotenv import load_dotenv
import os
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.filters import regex
from modules.tele import telegraph_upload
from modules.imdbb import imdb_callback, imdb_search

load_dotenv()
api_id = int(os.getenv("api_id"))
api_hash = os.getenv("api_hash")
bot_token = os.getenv("bot_token")

app = Client("imdb_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


@app.on_message(filters.command("start"))  # Respond in both private & groups
async def start(_, message):
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
║┣⪼🗣️ʟᴀɴɢᴜᴀɢᴇ : <a href=https://www.python.org>ᴘʏᴛʜᴏɴ3</a>
║┣⪼📚ʟɪʙʀᴀʀʏ : <a href=https://github.com/pyrogram>ᴘʏʀᴏɢʀᴀᴍ</a> 
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
* /about - To see Bot Stats
    ''')

app.add_handler(MessageHandler(telegraph_upload, filters.command("tgm")))
app.add_handler(MessageHandler(imdb_search, filters.command("imdb")))
app.add_handler(CallbackQueryHandler(imdb_callback, filters=regex(r'^imdb')))
# Start the bot
print("Bot Is Running")
app.run()
