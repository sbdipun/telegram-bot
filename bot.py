from pyrogram import Client, filters
from pyrogram.types import Message
import ffmpeg
import random
import os
import re
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

# Function to extract random screenshots from video
def generate_screenshots(video_path, count=10):
    file_duration = int(ffmpeg.probe(video_path)['format']['duration'].split('.')[0])
    points = sorted(random.sample(range(file_duration), count))
    screenshots = []
    for point in points:
        img_file = f"{point}.png"
        (
            ffmpeg
                .input(video_path, ss=point)
                .output(img_file, vframes=1)
                .run(capture_stdout=True, capture_stderr=True)
        )
        screenshots.append(img_file)
    return screenshots

# Remove created files to avoid clutter
def cleanup_files(file_list):
    for file_path in file_list:
        if os.path.exists(file_path):
            os.remove(file_path)

app = Client(api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
def start(client, message: Message):
    message.reply_text("Welcome! I Can Generate High Quality PNG Screenshots Of a Video. Just a Media file and Reply /ss.")

@app.on_message(filters.command("ss") & filters.reply & filters.video)
def screenshot(client, message: Message):
    try:
        video_message = message.reply_to_message
        
        # Download video file
        video_file_path = client.download_media(video_message)
        screenshots = generate_screenshots(video_file_path)

        # Send screenshots
        for screenshot in screenshots:
            message.reply_document(screenshot)

        # Cleanup
        cleanup_files(screenshots)
        cleanup_files([video_file_path])
    except Exception as e:
        message.reply_text("An error occurred: " + str(e))

if __name__ == '__main__':
    while True:
        try:
            app.run()
        except KeyboardInterrupt:
            print("Bot stopped by user")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Bot restarting...")
