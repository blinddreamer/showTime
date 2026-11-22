FROM python:3.11-slim

# Pull Debian security fixes not yet in the base image
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
# setuptools/wheel ship with the base image and are not needed at runtime (vendored CVEs)
RUN pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y setuptools wheel

COPY . .

CMD ["python", "bot.py"]
