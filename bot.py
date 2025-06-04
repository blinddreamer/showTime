import os
import re
import discord
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Enable intents with message content
intents = discord.Intents.default()
intents.message_content = True

# Create Discord client with intents
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    # Set the bot's status to "Playing EVE Online"
    await client.change_presence(activity=discord.Game(name="EVE Online"))
    print("Bot is ready and status set.")

@client.event
async def on_message(message):
    # Print every message to help debug
    print(f"Message from {message.author}: {message.content!r}")

    # Ignore messages sent by the bot itself
    if message.author == client.user:
        print("Ignoring own message.")
        return

    # Regex to find times like 19:00ET, 9:05et, etc.
    match = re.search(r'(\d{1,2}):(\d{2})ET', message.content, re.IGNORECASE)
    if match:
        print("EVE time pattern matched!")

        hour, minute = map(int, match.groups())

        # Build a datetime object for today at the given EVE time
        now_utc = datetime.utcnow()

        # EVE Time is UTC+4, so subtract 4 hours to get UTC time
        eve_time_utc = now_utc.replace(hour=hour, minute=minute, second=0, microsecond=0) - timedelta(hours=4)

        # Convert to Unix timestamp (seconds since epoch)
        timestamp = int(eve_time_utc.replace(tzinfo=timezone.utc).timestamp())

        # Format for Discord's timestamp markdown (will display in user's local timezone)
        replacement = f"<t:{timestamp}:f> (your local time)"

        try:
            # Edit the original message to add converted time on a new line
            new_content = f"{message.content}\n🕒 {replacement}"
            await message.edit(content=new_content)
            print("Message edited successfully.")

            # React with fire emoji
            await message.add_reaction("🔥")
            print("Reaction added successfully.")

        except discord.Forbidden:
            print("Permission error: cannot edit message or add reaction.")
        except discord.HTTPException as e:
            print(f"Discord HTTP error: {e}")

    else:
        print("No EVE time found in this message.")

print(f"Starting bot with token prefix: {TOKEN[:5]}...")  # For debug, never show full token
client.run(TOKEN)
