import asyncio
import os
import time
import math
import requests
from telethon import TelegramClient
from dotenv import load_dotenv             
from progress_for_telethon import progress2

# Your Pixel bot logic
async def process_pixel_command(event):
    message_text = event.message.text
    args = message_text.split()[1:]

    if len(args) == 1:  
        download_url = args[0]
        await event.reply("Please reply to the original download message with the desired filename (no extension needed).")

        user_reply =  await event.get_reply_message()
        file_name = user_reply.message.strip()

        # Infer file extension
        extension = download_url.rsplit('.', 1)[-1]  
        file_name += "." + extension 

        await download_and_upload(event, download_url, file_name)

    elif len(args) == 2: 
        download_url = args[0]
        file_name = args[1]
        await download_and_upload(event, download_url, file_name)
    else:
        await event.reply("Incorrect command format. Usage: /pixel <download_link> [optional_filename]")

async def download_and_upload(event, download_url, file_name):
    try:
        # Download with Progress Bar
        start = time.time()  
        async with TelegramClient('temp_session', api_id, api_hash) as temp_client:
            async with temp_client.download_file(download_url, file=file_name) as download_progress:  
                async for chunk in download_progress:
                    await event.reply(file=chunk)
                    await progress2(download_progress.downloaded_bytes, download_progress.total_bytes_expected, event, start, "Downloading", file_name)

        # Upload with Progress Bar:
        start = time.time() 
        async for chunk in event.client.iter_upload(file=file_name):
            await progress2(chunk.current_bytes, chunk.total_bytes, event, start, "Uploading")

        # Pixeldrain Upload (same as before)
        response = requests.post(
            PIXELDRAIN_API_URL,
            data={"name": file_name, "anonymous": True},
            files={"file": open(file_name, 'rb')}  
        )
        response.raise_for_status() 
        resp = response.json()
        await event.reply(f"https://pixeldrain.com/u/{resp['id']}")

    except requests.exceptions.RequestException as e:
        await event.reply(f"Error downloading file: {e}")

# ... (Rest of your bot setup functions and main function) 
