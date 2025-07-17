import os
import json
import psycopg2
from datetime import datetime
from ultralytics import YOLO
from dotenv import load_dotenv

load_dotenv()

# Load YOLO model
model = YOLO('yolov8n.pt')  # Use nano model for speed

# Connect to database
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=os.getenv("POSTGRES_PORT")
)
cursor = conn.cursor()

# Create table for detection results
cursor.execute("""
CREATE TABLE IF NOT EXISTS fct_image_detections (
    id SERIAL PRIMARY KEY,
    message_id BIGINT REFERENCES raw_telegram_messages(id),
    detected_object_class TEXT,
    confidence_score FLOAT,
    bbox_x1 FLOAT,
    bbox_y1 FLOAT,
    bbox_x2 FLOAT,
    bbox_y2 FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
conn.commit()

# Get messages with images
cursor.execute("""
SELECT id, image_path FROM raw_telegram_messages 
WHERE has_media = true AND image_path IS NOT NULL
""")
messages_with_images = cursor.fetchall()

for message_id, image_path in messages_with_images:
    if os.path.exists(image_path):
        try:
            # Run YOLO detection
            results = model(image_path)
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get detection info
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        coords = box.xyxy[0]
                        class_name = model.names[cls]
                        
                        # Insert into database
                        cursor.execute("""
                            INSERT INTO fct_image_detections 
                            (message_id, detected_object_class, confidence_score, 
                             bbox_x1, bbox_y1, bbox_x2, bbox_y2)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (
                            message_id, class_name, conf,
                            float(coords[0]), float(coords[1]), 
                            float(coords[2]), float(coords[3])
                        ))
            
            print(f"Processed image for message {message_id}")
            
        except Exception as e:
            print(f"Error processing image for message {message_id}: {e}")
    else:
        print(f"Image not found: {image_path}")

conn.commit()
cursor.close()
conn.close()

print("YOLO detection completed!") 