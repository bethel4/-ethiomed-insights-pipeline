# miot-pipeline

This project is a data pipeline for Ethiomed Insights, leveraging Telegram, Postgres, dbt, FastAPI, Dagster, and more.

## Project Structure

```
miot-pipeline/
├── api/
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

## Setup

1. Copy `.env` and fill in your credentials.
2. Build and start the stack:
   ```bash
   docker-compose up --build
   ``` 