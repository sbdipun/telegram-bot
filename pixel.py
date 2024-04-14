import asyncio
import requests
import tqdm
from telethon import TelegramClient

# Pixeldrain API settings
PIXELDRAIN_API_URL = "https://pixeldrain.com/api/file"

# Your formatting function
def format_bytes(num_bytes):
    if num_bytes < 1024:
        return f"{num_bytes} B"
    elif num_bytes < 1024 ** 2:
        return f"{num_bytes / 1024:.2f} KB"
    elif num_bytes < 1024 ** 3:
        return f"{num_bytes / 1024 ** 2:.2f} MB"
    else:
        return f"{num_bytes / 1024 ** 3:.2f} GB"

async def process_pixel_command(event):
    message_text = event.message.text
    args = message_text.split()[1:]

    download_url = args[0]  

    # Prompt for custom filename (if desired)
    custom_filename = None
    while not custom_filename:
        user_response = await event.reply("Enter a custom filename for the downloaded file (or press Enter to use the default name): ")
        custom_filename = user_response.message.strip()
        if not custom_filename:
            await event.reply("Using default filename based on download URL.")
            break  

    await download_and_upload(event, download_url, custom_filename)

async def download_and_upload(event, download_url, file_name):
    try:
        # Download with Progress Bar
        async with TelegramClient('temp_session', api_id, api_hash) as temp_client:
            async with temp_client.download_file(download_url, file=file_name) as download_progress:  
                async for chunk in download_progress:
                    await event.reply( 
                        f"Downloading: {format_bytes(download_progress.downloaded_bytes)} of {format_bytes(download_progress.total_bytes_expected)}",
                        file=chunk,
                        progress_bar=True
                    )

        # Upload with Progress Bar:
        await event.respond(
            "Uploading to Pixeldrain...", 
            file=file_name,
            progress_bar=True
        )  

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

# ... (Rest of your bot setup functions and main function, e.g., connecting to Telegram)
            
