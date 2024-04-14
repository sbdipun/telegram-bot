import asyncio
import requests
import tqdm
from telethon import TelegramClient
from telethon.utils import format_bytes

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
        progress_dots = "●●●●●●●●●●"  
        async with TelegramClient('temp_session', api_id, api_hash) as temp_client:
            async with temp_client.download_file(download_url, file=file_name) as download_progress:  
                async for chunk in download_progress:
                    progress = int(10 * download_progress.downloaded_bytes / download_progress.total_bytes_expected)
                    await event.reply( 
                        f"Downloading: {format_bytes(download_progress.downloaded_bytes)} of {format_bytes(download_progress.total_bytes_expected)} "
                        f"{progress_dots[:progress]}{'■' * (10 - progress)}",
                        file=chunk,
                    )  

        # Upload with Progress Bar:
        progress_dots = "●●●●●●●●●●" 
        async for chunk in event.client.iter_upload(file=file_name):
            progress = int(10 * chunk.current_bytes / chunk.total_bytes)
            await event.respond(
                f"Uploading to Pixeldrain: {format_bytes(chunk.current_bytes)} of {format_bytes(chunk.total_bytes)} " 
                f"{progress_dots[:progress]}{'■' * (10 - progress)}"  
            ) 

        # ... (Rest of your Pixeldrain upload code)

    except requests.exceptions.RequestException as e:
        await event.reply(f"Error downloading file: {e}")

# ... (Rest of your bot setup functions and main function)
