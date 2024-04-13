import asyncio
import requests
import argparse

PIXELDRAIN_API_URL = "https://pixeldrain.com/api/file"

async def download_and_upload(event, download_url, file_name):
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        await upload_to_pixeldrain(event, response.content, file_name)

    except requests.exceptions.RequestException as e:
        await event.reply(f"Error downloading file: {e}")

async def upload_to_pixeldrain(event, file_content, file_name):
    try:
        response = requests.post(
            PIXELDRAIN_API_URL,
            data={"name": file_name, "anonymous": True},
            files={"file": file_content}
        )
        response.raise_for_status()
        resp = response.json()
        await event.reply(f"https://pixeldrain.com/u/{resp['id']}")
    except requests.exceptions.RequestException as e:
        await event.reply(f"Error uploading file: {e}")

# Updated to handle the rename functionality
async def process_pixel_command(event):
    message_text = event.message.text  
    args = message_text.split()[1:] 

    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help='Custom file name with extension')
    parsed_args = parser.parse_args(args)

    if parsed_args.name:
        file_name = parsed_args.name
    else:
        download_url = args[0]
        file_name = download_url.split('/')[-1]  

    await download_and_upload(event, download_url, file_name)
