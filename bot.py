import os
import re
import discord
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    # Set custom status (playing EVE Online)
    await client.change_presence(activity=discord.Game(name="EVE Online"))

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Look for times like 19:00ET in the message
    match = re.search(r'(\d{1,2}):(\d{2})ET', message.content)
    if match:
        hour, minute = map(int, match.groups())

        # Convert ET (assumed UTC-4) to UTC by adding 4 hours
        utc_time = datetime.utcnow().replace(hour=hour, minute=minute, second=0, microsecond=0) + timedelta(hours=4)

        # Create a Discord timestamp for local time display
        timestamp = int(utc_time.replace(tzinfo=timezone.utc).timestamp())
        replacement = f"<t:{timestamp}:f> (your local time)"

        try:
            # Edit original message to append converted time
            await message.edit(content=f"{message.content}\n🕒 {replacement}")
            # React with fire emoji
            await message.add_reaction("🔥")
        except discord.Forbidden:
            print("Missing permissions to edit message or add reaction.")
        except discord.HTTPException as e:
            print(f"Failed to edit message: {e}")

client.run(TOKEN)
