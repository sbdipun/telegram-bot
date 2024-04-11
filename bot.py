from pyrogram import Client, filters
from pyrogram.types import Message
import ffmpeg
import random
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

if not api_id or not api_hash or not bot_token:
    raise ValueError("API_ID, API_HASH, and BOT_TOKEN environment variables must be set")

# Async function to extract random screenshots from video
async def generate_screenshots(video_path, count=10):
    file_duration = int(ffmpeg.probe(video_path)['format']['duration'].split('.')[0])
    points = sorted(random.sample(range(file_duration), count))
    screenshots = []
    for idx, point in enumerate(points):
        img_file = f"screenshot_{idx}.png"
        await asyncio.to_thread(
            ffmpeg.input(video_path, ss=point)
            .output(img_file, vframes=1)
            .run,
            capture_stdout=True,
            capture_stderr=True
        )
        screenshots.append(img_file)
    return screenshots

# Async function to remove created files to avoid clutter
async def cleanup_files(file_list):
    for file_path in file_list:
        if os.path.exists(file_path):
            os.remove(file_path)

app = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text("Welcome! I Can Generate High-Quality PNG Screenshots Of a Video. Just Send a Media File and Reply /ss.")

@app.on_message(filters.command("ss") & filters.reply & filters.video)
async def screenshot(client, message: Message):
    try:
        video_message = message.reply_to_message
        
        # Download video file
        video_file_path = await client.download_media(video_message)
        screenshots = await generate_screenshots(video_file_path)

        # Send screenshots
        for screenshot in screenshots:
            await message.reply_document(screenshot)

        # Cleanup
        await cleanup_files(screenshots)
        await cleanup_files([video_file_path])
    except Exception as e:
        await message.reply_text("An error occurred: " + str(e))

if name == 'main':
    print("Bot is running...")
    app.run()
