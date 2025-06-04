import os
import re
import discord
from datetime import datetime, timedelta, timezone
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ET_OFFSET = -4  # adjust depending on Daylight Saving Time

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

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
