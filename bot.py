import os
import re
import discord
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Setup intents to read message content
intents = discord.Intents.default()
intents.message_content = True

# Create client
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    # Set bot status to playing EVE Online
    await client.change_presence(activity=discord.Game(name="EVE Online"))
    print("Bot is ready and status set.")

@client.event
async def on_message(message):
    print(f"Received message from {message.author}: {message.content!r}")

    # Ignore messages from ourselves
    if message.author == client.user:
        print("Message from self, ignoring.")
        return

    # Regex to find times like 19:00ET (case insensitive)
    match = re.search(r'(\d{1,2}):(\d{2})ET', message.content, re.IGNORECASE)
    if match:
        print("Matched EVE time in message!")

        hour, minute = map(int, match.groups())

        # Convert EVE Time (UTC+4) to UTC for Discord timestamp:
        # EVE time is UTC +4, so to get UTC, subtract 4 hours
        # But since we build a datetime in utcnow and replace hour/minute,
        # we add 4 hours to utcnow (that’s how we did it previously),
        # let's be consistent and do it like this:

        # First get today's date in UTC
        now_utc = datetime.utcnow()
        # Create datetime with the matched hour/minute but today’s date in UTC
        eve_time_utc = now_utc.replace(hour=hour, minute=minute, second=0, microsecond=0) - timedelta(hours=4)

        # Get unix timestamp for Discord formatting
        timestamp = int(eve_time_utc.replace(tzinfo=timezone.utc).timestamp())

        # Create replacement string for local Discord client time display
        replacement = f"<t:{timestamp}:f> (your local time)"

        try:
            # Edit original message to append converted time
            new_content = f"{message.content}\n🕒 {replacement}"
            await message.edit(content=new_content)

            # Add fire emoji reaction
            await message.add_reaction("🔥")

            print("Edited message and added reaction successfully.")
        except discord.Forbidden:
            print("Missing permissions to edit message or add reaction.")
        except discord.HTTPException as e:
            print(f"Failed to edit message: {e}")
    else:
        print("No EVE time match found in message.")

# Run the bot
client.run(TOKEN)
