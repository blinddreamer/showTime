# Discord Time Converter Bot ⏰🔥

A simple Discord bot that listens for `HH:MMET` time mentions (like `19:00ET`) and:

- Converts them to **EVE Time (UTC)**
- Replies with the converted time
- Reacts to the message with a 🔥 emoji

Perfect for coordinating fleet ops across time zones.

---

## 🐳 Run with Docker

```bash
docker build -t discord-timebot .
docker run -e DISCORD_TOKEN=your_token_here discord-timebot
```
