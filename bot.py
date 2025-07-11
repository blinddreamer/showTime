import os
import re
import discord
from datetime import datetime, timezone
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

    # Match multiple times like "13:00et" or "15:00 et"
    matches = re.findall(r'(\d{1,2}):(\d{2})\s*et', message.content, re.IGNORECASE)

    if matches:
        responses = []
        for hour_str, minute_str in matches:
            try:
                hour, minute = int(hour_str), int(minute_str)

                # Convert to UTC (EVE time)
                now = datetime.utcnow()
                eve_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

                # If the time has already passed today, assume it's for tomorrow
                if eve_time < now:
                    eve_time += timedelta(days=1)

                timestamp = int(eve_time.replace(tzinfo=timezone.utc).timestamp())
                discord_timestamp = f"<t:{timestamp}:f>"
                responses.append(f"`{hour:02}:{minute:02}ET` → {discord_timestamp}")

                print(f"✅ Time converted: {hour:02}:{minute:02}ET")

            except Exception as e:
                print(f"❌ Error while processing time: {e}")

        if responses:
            await message.channel.send("🕒 " + " | ".join(responses))
            await message.add_reaction("🔥")

# Start the bot
client.run(TOKEN)
