import os
import json
import logging
from datetime import datetime
from telethon.sync import TelegramClient
from dotenv import load_dotenv

load_dotenv()

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/scrape_telegram.log"),
        logging.StreamHandler()
    ]
)

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
channels = [
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma",
    "https://t.me/lobelia4cosmetics"  # Add more if needed
]

client = TelegramClient("session", api_id, api_hash)
client.start()

total_messages = 0
total_images = 0
total_errors = 0

for channel in channels:
    try:
        logging.info(f"Scraping channel: {channel}")
        messages_data = []
        today = datetime.today().strftime('%Y-%m-%d')
        name = channel.split("/")[-1]

        for message in client.iter_messages(channel, limit=100):
            msg_dict = {
                "id": message.id,
                "text": message.text,
                "date": str(message.date),
                "has_media": message.media is not None,
                "media_type": str(type(message.media)) if message.media else None
            }
            total_messages += 1
            # Download image if present
            if message.media:
                img_dir = f"data/raw/telegram_images/{today}"
                os.makedirs(img_dir, exist_ok=True)
                img_path = f"{img_dir}/{name}_{message.id}.jpg"
                try:
                    client.download_media(message, img_path)
                    msg_dict["image_path"] = img_path
                    total_images += 1
                except Exception as e:
                    logging.error(f"Failed to download image for message {message.id}: {e}")
                    msg_dict["image_path"] = None
                    total_errors += 1
            messages_data.append(msg_dict)

        os.makedirs(f"data/raw/telegram_messages/{today}", exist_ok=True)
        with open(f"data/raw/telegram_messages/{today}/{name}.json", "w") as f:
            json.dump(messages_data, f, indent=2)
        logging.info(f"Finished scraping {channel}")
    except Exception as e:
        logging.error(f"Error scraping {channel}: {e}")
        total_errors += 1

logging.info(f"Scraping completed: {total_messages} messages, {total_images} images, {total_errors} errors.")
print("Scraping completed.") 