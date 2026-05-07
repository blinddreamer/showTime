import os
import re
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

TIME_PATTERN = re.compile(r'(\d{1,2}):(\d{2})\s*et', re.IGNORECASE)


def convert_et_times(text: str) -> list[str]:
    matches = TIME_PATTERN.findall(text)
    results = []
    now = datetime.utcnow()

    for hour_str, minute_str in matches:
        try:
            hour, minute = int(hour_str), int(minute_str)
            eve_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if eve_time < now:
                eve_time += timedelta(days=1)
            ts = int(eve_time.replace(tzinfo=timezone.utc).timestamp())
            results.append(f"`{hour:02}:{minute:02}ET` → <t:{ts}:t>")
        except Exception as e:
            print(f"❌ Error converting time: {e}")

    return results


class ShowTimeView(discord.ui.View):
    def __init__(self, conversions: list[str]):
        super().__init__(timeout=600)
        self.conversions = conversions

    @discord.ui.button(label="Show in my timezone", emoji="🕒", style=discord.ButtonStyle.secondary)
    async def show_time(self, interaction: discord.Interaction, _button: discord.ui.Button):
        await interaction.response.send_message(
            "🕒 " + " | ".join(self.conversions),
            ephemeral=True,
        )


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(activity=discord.Game(name="EVE Online"))


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    print(f"📨 Message from {message.author}: {message.content}")

    conversions = convert_et_times(message.content)
    if conversions:
        view = ShowTimeView(conversions)
        await message.channel.send(
            "🕒 EVE times detected in this post",
            view=view,
            reference=message,
            mention_author=False,
        )

    await bot.process_commands(message)


@bot.tree.command(name="et", description="Convert an EVE Time (ET/UTC) to your local timezone")
@app_commands.describe(hour="Hour in EVE time (0-23)", minute="Minute (0-59)")
async def et_slash(interaction: discord.Interaction, hour: int, minute: int):
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        await interaction.response.send_message(
            "❌ Hour must be 0–23 and minute must be 0–59.",
            ephemeral=True,
        )
        return

    conversions = convert_et_times(f"{hour:02}:{minute:02}ET")
    if conversions:
        await interaction.response.send_message(
            "🕒 " + " | ".join(conversions),
            ephemeral=True,
        )
    else:
        await interaction.response.send_message("❌ Could not convert that time.", ephemeral=True)


bot.run(TOKEN)
