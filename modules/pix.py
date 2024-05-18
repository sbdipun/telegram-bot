import asyncio
import aiohttp
from pyrogram import Client, filters

@Client.on_message(filters.command("pixel"))
async def pixel(_, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a URL after the command.")
        return

    url = message.command[1]
    file_name = url.split('/')[-1]

    async with aiohttp.ClientSession() as session:
        # Download the file
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    await message.reply_text("Failed to download the file.")
                    return
                data = await response.read()
        except Exception as e:
            await message.reply_text(f"Error downloading the file: {str(e)}")
            return

        # Upload file to Pixeldrain
        try:
            files = {'file': (file_name, data)}
            async with session.post("https://pixeldrain.com/api/file", data={"name": file_name}, files=files) as response:
                if response.status != 200:
                    await message.reply_text("Failed to upload the file to Pixeldrain.")
                    return
                result_json = await response.json()
                file_id = result_json.get('id')
                await message.reply_text(f"File uploaded to Pixeldrain! View at https://pixeldrain.com/u/{file_id}")
        except Exception as e:
            await message.reply_text(f"Error uploading file to Pixeldrain: {str(e)}")
