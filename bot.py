import os
import re
import discord
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Necessary to read message content

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.change_presence(activity=discord.Game(name="EVE Online"))

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    print(f"Message received: '{message.content}' from {message.author}")

    # Regex to find time like 19:00ET (case sensitive)
    match = re.search(r'(\d{1,2}):(\d{2})ET', message.content)
    if match:
        print("Detected time pattern in message!")

        hour, minute = map(int, match.groups())

        # Current UTC date+time, then replace hour & minute from message,
        # then add 4 hours to convert ET (UTC-4) to UTC
        utc_time = datetime.utcnow().replace(hour=hour, minute=minute, second=0, microsecond=0) + timedelta(hours=4)

        # Get unix timestamp for Discord timestamp formatting
        timestamp = int(utc_time.replace(tzinfo=timezone.utc).timestamp())
        replacement = f"<t:{timestamp}:f> (your local time)"

        try:
            # Append the converted time to the original message
            new_content = f"{message.content}\n🕒 {replacement}"
            await message.edit(content=new_content)
            await message.add_reaction("🔥")
        except discord.Forbidden:
            print("Missing permissions to edit message or add reaction.")
        except discord.HTTPException as e:
            print(f"Failed to edit message: {e}")

client.run(TOKEN)
