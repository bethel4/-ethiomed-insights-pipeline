# Ethiomed Insights Pipeline

## Project Overview
A modern ELT pipeline for scraping, enriching, and analyzing Ethiopian medical business data from Telegram channels. The pipeline uses Telethon for scraping, YOLOv8 for image enrichment, dbt for modeling, and FastAPI for analytics.

## Folder Structure
```
miot-pipeline/
├── api/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── crud.py
├── data/
│   └── raw/
├── dbt_project/
├── docker/
├── etl/
├── orchestration/
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Setup Instructions
1. Clone the repo and install dependencies.
2. Add your `.env` file with Telegram and Postgres credentials.
3. Start Docker containers:
   ```bash
   docker-compose up -d
   ```
4. Scrape Telegram data:
   ```bash
   docker-compose exec app python etl/scrape_telegram.py
   ```
5. Load data to Postgres:
   ```bash
   docker-compose exec app python etl/load_to_postgres.py
   ```
6. Run YOLO enrichment:
   ```bash
   docker-compose exec app python etl/run_yolo_detection.py
   ```
7. Run dbt models:
   ```bash
   cd dbt_project
   dbt run
   dbt test
   ```
8. Start the FastAPI server:
   ```bash
   uvicorn api.main:app --reload
   ```
   or, if using Docker Compose, ensure the API service is included and run:
   ```bash
   docker-compose up -d
   ```

## API Usage
- Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation.

### Example Endpoints
- **Health Check:** `GET /api/health`
- **Top Products:** `GET /api/reports/top-products?limit=5`
- **Channel Activity:** `GET /api/channels/{channel_name}/activity`
- **Search Messages:** `GET /api/search/messages?query=vitamin&limit=5`

## Pipeline Diagram
```mermaid
flowchart TD
    A[Telegram Channels] -->|Telethon| B[Raw JSON Files\ndata/raw/telegram_messages/]
    B -->|Python ETL| C[Postgres Table\nraw_telegram_messages]
    C -->|dbt| D[Staging Model\nstg_telegram_messages]
    D -->|dbt| E[Mart Model\nfct_messages]
    C -->|YOLO| F[Detection Table\nfct_image_detections]
    F -->|dbt| G[Enriched Mart\nfct_enriched_messages]
    G -->|FastAPI| H[Analytical API]
```

## Known Issues / TODOs
- Dependency conflicts may occur with numpy/decorator/tensorflow; see pip warnings.
- Add more dbt tests and documentation.
- Add more FastAPI endpoints for analytics.
- Add Dagster orchestration (Task 5).

## Contact
For questions, contact the project maintainer. 