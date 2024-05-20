import random
import logging
import string
from pyrogram import Client, filters
import asyncio


@Client.on_message(filters.command("pass"))
async def generate_password(_, message):
    """Generates a random password and sends it to the user."""

    try:
        # Customize password length and characters here
        length = 10

        # Ensure at least one of each type is included
        password = [
            random.choice(string.ascii_letters),
            random.choice(string.digits),
            random.choice(string.punctuation)
        ]

        # Fill remaining characters randomly
        password += [random.choice(string.ascii_letters + string.digits + string.punctuation)
                     for _ in range(length - 3)]

        # Shuffle the password for better randomness
        random.shuffle(password)

        # Join into a string
        password = ''.join(password)

        # Send the password
        sent_message = await message.reply_text(f"**Your Password:**\n<code>{password}</code>")
        logging.info(f"Successfully generated password")

        # Wait for 15 seconds and delete the message
        await asyncio.sleep(15)
        await sent_message.delete()
        logging.info("Password message deleted")

    except Exception as e:
        logging.error(f"Error generating password: {e}")
        await message.reply_text("An error occurred while generating the password.")
