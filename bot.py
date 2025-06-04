import os
import re
import discord
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Setup intents
intents = discord.Intents.default()
intents.message_content = True

# Create Discord client
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user} (ID: {client.user.id})")
    await client.change_presence(activity=discord.Game(name="EVE Online"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(f"📨 Message from {message.author}: {message.content}")

    match = re.search(r'(\d{1,2}):(\d{2})ET', message.content, re.IGNORECASE)
    if match:
        hour, minute = map(int, match.groups())

        try:
            # EVE time = UTC, no DST. Assume message means UTC time
            eve_time = datetime.utcnow().replace(hour=hour, minute=minute, second=0, microsecond=0)
            timestamp = int(eve_time.replace(tzinfo=timezone.utc).timestamp())
            discord_timestamp = f"<t:{timestamp}:f>"

            await message.channel.send(f"🕒 {discord_timestamp}")
            await message.add_reaction("🔥")
            print(f"✅ Time converted and replied for: {hour}:{minute}ET")

        except Exception as e:
            print(f"❌ Error while processing time: {e}")

# Start the bot
client.run(TOKEN)
