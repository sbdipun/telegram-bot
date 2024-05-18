import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

# ... (Your other imports and bot setup) ...

DOWNLOAD_LOCATION = "./DOWNLOADS/"  # Directory to store downloaded files


@Client.on_message(filters.command("pixurl"))
async def upload_from_url(_, message: Message):
    """Handle the /pixurl command for uploading from URL."""
    args = message.text.split()  # Split the command into arguments
    url = args[1] if len(args) > 1 else None  # Get the URL
    new_filename = args[2] if len(args) > 2 else None  # Get the new filename

    if not url:
        return await message.reply_text("Please provide a URL after the command.")  # Added new_filename argument

    try:
        file_extension = os.path.splitext(url)[1]  # Get the file extension from the URL

        # Use the new filename if provided, otherwise keep the original filename
        file_name = f"{new_filename or url.split('/')[-1]}"

        # If no file extension is provided in the new filename, use the original extension
        if not new_filename.endswith(file_extension):
            file_name += file_extension

        file_path = os.path.join(DOWNLOAD_LOCATION, file_name)

        await message.reply_text("Downloading from URL...")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception if download fails

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        await upload_to_pixeldrain(file_path, message) 

    except Exception as e:
        print(f"Error downloading or uploading from URL: {e}")
        await message.reply_text(f"An error occurred: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)  # Clean up the downloaded file


async def upload_to_pixeldrain(file_path, message):
    """Uploads a file to Pixeldrain and sends the link."""
    try:
        with open(file_path, "rb") as f:
            file_content = f.read()

        await message.reply_text("Uploading to Pixeldrain...")

        response = requests.post(
            "https://pixeldrain.com/api/file",
            data={"name": file_path, "anonymous": True},
            files={"file": file_content}
        )

        if response.status_code == 200:
            resp = response.json()
            link = f"https://pixeldrain.com/u/{resp['id']}"
            await message.reply_text(f"File uploaded to Pixeldrain:\n{link}")
        else:
            await message.reply_text(f"Pixeldrain upload failed with status code: {response.status_code}")

    except Exception as e:
        print(f"Error uploading to Pixeldrain: {e}")
        await message.reply_text(f"An error occurred: {e}")
