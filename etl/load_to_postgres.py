import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=os.getenv("POSTGRES_PORT")
)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS raw_telegram_messages (
    id BIGINT PRIMARY KEY,
    text TEXT,
    date TIMESTAMP,
    has_media BOOLEAN,
    media_type TEXT
);
""")
conn.commit()

base_dir = "data/raw/telegram_messages"
for date_folder in os.listdir(base_dir):
    full_path = os.path.join(base_dir, date_folder)
    for file in os.listdir(full_path):
        with open(os.path.join(full_path, file)) as f:
            messages = json.load(f)
            for msg in messages:
                try:
                    cursor.execute("""
                        INSERT INTO raw_telegram_messages (id, text, date, has_media, media_type)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING;
                    """, (msg["id"], msg["text"], msg["date"], msg["has_media"], msg["media_type"]))
                except Exception as e:
                    print(f"Error inserting message: {e}")
conn.commit()
cursor.close()
conn.close() 