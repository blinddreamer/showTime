import os
import re
import discord
from datetime import datetime, timedelta, timezone
from discord.ext import commands
from dotenv import load_dotenv

# Load token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot with activity status
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    activity=discord.Game(name="EVE Online"),
    status=discord.Status.online
)

ET_OFFSET = -4  # Adjust for DST (can be dynamic if needed)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    match = re.search(r'(\d{1,2}):(\d{2})ET', message.content)
    if match:
        hour, minute = map(int, match.groups())
        et_time = datetime.utcnow().replace(hour=hour, minute=minute, second=0, microsecond=0) - timedelta(hours=ET_OFFSET)
        timestamp = int(et_time.replace(tzinfo=timezone.utc).timestamp())

        reply = f"🕒 <t:{timestamp}:f> (your local time)"
        await message.channel.send(reply)
        await message.add_reaction("🔥")

    await bot.process_commands(message)

# Run the bot
bot.run(TOKEN)
