from telethon import events

@events.register(events.NewMessage(pattern='/info'))
async def info_handler(event):
    user = await event.client.get_entity(event.sender_id)
    user_info_string = f"User ID: {user.id}\nFirst Name: {user.first_name}\nUsername: @{user.username}\nUser Link: [User Link](tg://user?id={user.id})"
    await event.reply(user_info_string, parse_mode='md')
  
