# Discord Time Converter Bot ⏰

A Discord bot that detects EVE Time (ET/UTC) mentions in chat and helps players convert them to their local timezone.

Perfect for coordinating fleet ops across time zones.

---

## Features

### Automatic ET detection

When any message contains a time in `HH:MM ET` format (e.g. `19:00ET` or `15:30 et`), the bot replies with a button attached to the original message. Clicking **"🕒 Show in my timezone"** shows the converted local time — visible only to you. The button stays active for **24 hours** after the message is posted.

### `/et` slash command

Use `/et` to manually convert an EVE time to your local timezone. Discord prompts for two separate fields:

- **hour** — EVE time hour (0–23)
- **minute** — EVE time minute (0–59)

The result is shown only to you (ephemeral), so it won't clutter the channel.

---

## 🐳 Run with Docker

```bash
docker build -t discord-timebot .
docker run -e DISCORD_TOKEN=your_token_here discord-timebot
```
