import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

# ... (Your other imports and bot setup) ...

DOWNLOAD_LOCATION = "./DOWNLOADS/"  # Directory to store downloaded files


@Client.on_message(filters.command("pixurl"))
async def upload_from_url(client, message: Message):  
    """Handle the /pixurl command for uploading from URL."""
    if len(message.command) < 2:
        return await message.reply_text("Please provide a URL after the command. E.g., `/pixurl https://example.com/image.jpg [optional_new_filename.ext]`")  

    url = message.command[1]
    new_filename = message.command[2] if len(message.command) > 2 else None

    # Basic URL validation
    if not url.startswith("http"):
        return await message.reply_text("Invalid URL. Please provide a valid link.")

    try:
        file_extension = os.path.splitext(url)[1] if new_filename is None else os.path.splitext(new_filename)[1]

        # Use the new filename if provided, otherwise keep the original filename
        file_name = f"{new_filename or url.split('/')[-1]}"

        # If no file extension is provided in the new filename, use the original extension
        if not new_filename or not new_filename.endswith(file_extension):
            file_name += file_extension

        file_path = os.path.join(DOWNLOAD_LOCATION, file_name)

        await message.reply_text("Downloading from URL...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        await upload_to_pixeldrain(file_path, message)  # Pass file_path

    except requests.exceptions.RequestException as e:
        await message.reply_text(f"Error downloading the file: {e}")
    except Exception as e:
        print(f"Error downloading or uploading from URL: {e}")
        await message.reply_text(f"An error occurred: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


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

    except FileNotFoundError as e: # Specific error for missing files
        await message.reply_text(f"File not found: {e}")
    except Exception as e:  # Catch-all for other errors
        print(f"Error uploading to Pixeldrain: {e}")
        await message.reply_text(f"An error occurred: {e}")


