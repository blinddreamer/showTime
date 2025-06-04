Discord Time Converter Bot ⏰🔥
A simple Discord bot that listens for HH:MMET time mentions (like 19:00ET) and:

Converts them to EVE Time (UTC)

Replies with the converted time

Reacts to the message with a 🔥 emoji

Perfect for coordinating fleet ops across time zones.

🐳 Run with Docker
bash
Copy
Edit
docker build -t discord-timebot .
docker run -e DISCORD_TOKEN=your_token_here discord-timebot
Or use a .env file:

env
Copy
Edit
DISCORD_TOKEN=your_token_here
Then:

bash
Copy
Edit
docker run --env-file .env discord-timebot
📂 Project Structure
bash
Copy
Edit
.
├── bot.py # Main bot logic
├── Dockerfile
├── requirements.txt
└── README.md
⚙️ Features
Detects HH:MMET in messages

Converts to EVE Time (UTC)
Replies + reacts with 🔥
