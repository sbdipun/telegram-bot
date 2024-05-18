import asyncio
import aiohttp
from pyrogram import Client, filters

@Client.on_message(filters.command("pixurl"))
async def pixel(_, message):

    # Get the URL from the command
    if len(message.command) < 2:
        return await message.reply_text("Please provide a URL after the command. E.g., `/pixurl https://example.com/image.jpg`")
    url = message.command[1]
    file_name = url.split('/')[-1]

    # Function to upload the file
    async def upload_to_pixeldrain(url, session, file_name, message):
        """Uploads a file to Pixeldrain and sends the link."""
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    await message.reply_text("Failed to download the file.")
                    return
                file_data = await response.read()

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

        except Exception as e:
            await message.reply_text(f"Error downloading the file: {str(e)}")
            return


    async with aiohttp.ClientSession() as session:
        await upload_to_pixeldrain(url, session, file_name, message)
