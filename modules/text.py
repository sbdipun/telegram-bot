from telethon import events, utils
import os

@events.register(events.NewMessage(pattern='/text'))
async def text_handler(event):
    if event.is_reply:
        replied_message = await event.get_reply_message()
        if replied_message.text:
            message_text = replied_message.text
            file_path = 'message.txt'
            with open(file_path, 'w') as file:
                file.write(message_text)

            await event.reply('Please enter a new name for the text file:')
            
            # Listen for the next message for renaming
            @events.register(events.NewMessage(incoming=True))
            async def rename_text_file(event):
                new_name = f'{event.text}.txt'
                os.rename(file_path, new_name)
                
                # Send the renamed text file to the user
                await event.client.send_file(event.chat_id, new_name, caption='Here is your file:')
                # Remove the event handler if you don't want further messages to trigger file renaming
                event.client.remove_event_handler(rename_text_file)
    else:
        await event.reply('Please reply to a text message.')
