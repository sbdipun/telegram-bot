import asyncio
import aiohttp
from pyrogram import Client, filters

@Client.on_message(filters.command("pixurl"))
async def pixel(_, message):
    # ... (Your URL extraction logic remains the same) ...

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    await message.reply_text("Failed to download the file.")
                    return
                file_data = await response.read()  # Renamed variable

        except Exception as e:
            await message.reply_text(f"Error downloading the file: {str(e)}")
            return

        # Prepare FormData with the correct file_data
        payload = aiohttp.FormData()
        payload.add_field('file', file_data, filename=file_name, content_type='application/octet-stream')

        # Upload file to Pixeldrain
        try:
            async with session.post("https://pixeldrain.com/api/file", data=payload) as response:
                if response.status != 200:
                    await message.reply_text("Failed to upload the file to Pixeldrain.")
                    return
                result_json = await response.json()
                file_id = result_json.get('id')
                await message.reply_text(f"File uploaded to Pixeldrain! View at https://pixeldrain.com/u/{file_id}")
        except Exception as e:
            await message.reply_text(f"Error uploading file to Pixeldrain: {str(e)}")
