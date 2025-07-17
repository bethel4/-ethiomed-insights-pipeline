# Ethiomed Insights Pipeline

## Project Overview
A modern end-to-end ELT pipeline for scraping, enriching, and analyzing Ethiopian medical business data from Telegram channels. The pipeline uses Telethon for scraping, YOLOv8 for image enrichment, dbt for data modeling, FastAPI for analytics, and Dagster for orchestration.

## 🎯 Completed Tasks

###  Task 0t Setup
- Complete folder structure with organized modules
- Environment configuration with `.env` file
- Docker setup with `Dockerfile` and `docker-compose.yml`
- Dependencies management with `requirements.txt`

###  Task1 Telegram Scraping & Data Lake
- Telethon-based scraper for Ethiopian medical channels
- Raw JSON data storage partitioned by date and channel
- Image downloads for YOLO enrichment
- Comprehensive logging and error handling

### ✅ Task2: Data Loading & dbt Modeling
- PostgreSQL data loading from raw JSON files
- dbt project setup with staging and mart models
- Data quality tests and documentation
- Automated data transformations

### ✅ Task 3: YOLO Image Enrichment
- YOLOv8bject detection on scraped images
- Detection results stored in PostgreSQL
- dbt models integrating detection data with messages
- Enriched analytics-ready datasets

### ✅ Task 4: FastAPI Analytical API
- RESTful API for business insights
- Database integration with SQLAlchemy
- Pydantic schemas for data validation
- Endpoints for top products, channel activity, and message search

### ✅ Task 5: Dagster Orchestration
- Complete pipeline orchestration with Dagster
- Automated scheduling for daily runs
- Monitoring and observability
- Error handling and retry logic

## 📁 Project Structure
```
-ethiomed-insights-pipeline/
├── api/                          # FastAPI application
│   ├── main.py                   # API entry point
│   ├── database.py               # Database connection
│   ├── schemas.py                # Pydantic models
│   └── crud.py                   # Database operations
├── data/                         # Data storage
│   └── raw/                      # Raw scraped data
├── dbt_project/                  # dbt data modeling
│   ├── models/
│   │   ├── staging/              # Staging models
│   │   └── marts/                # Mart models
│   └── profiles.yml              # dbt configuration
├── docker/                       # Docker configurations
├── etl/                          # ETL scripts
│   ├── scrape_telegram.py        # Telegram scraper
│   ├── load_to_postgres.py       # Data loader
│   ├── run_yolo_detection.py     # YOLO enrichment
│   └── test_telegram_connection.py
├── orchestration/                # Dagster orchestration
│   ├── jobs/
│   │   └── ethiomed_pipeline.py  # Main pipeline job
│   ├── ops/
│   │   ├── dbt_ops.py            # dbt operations
│   │   ├── postgres_ops.py       # Database operations
│   │   └── yolo_ops.py           # YOLO operations
│   └── schedules/
│       └── daily_schedule.py     # Pipeline scheduling
├── logs/                         # Application logs
├── docker-compose.yml            # Container orchestration
├── Dockerfile                    # Application container
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

##  Quick Start

### 1. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd -ethiomed-insights-pipeline

# Create and configure environment file
cp .env.example .env
# Edit .env with your credentials:
# - TELEGRAM_API_ID
# - TELEGRAM_API_HASH
# - TELEGRAM_PHONE
# - POSTGRES_URI
# - CHANNEL_NAMES (comma-separated)
```

### 2. Start Infrastructure
```bash
# Start all services
docker-compose up -d

# Verify services are running
docker-compose ps
```

### 3. Run the Complete Pipeline

#### Option A: Manual Execution
```bash
# 1rape Telegram data
docker-compose exec app python etl/scrape_telegram.py

# 2. Load data to PostgreSQL
docker-compose exec app python etl/load_to_postgres.py

# 3. Run YOLO enrichment
docker-compose exec app python etl/run_yolo_detection.py

# 4. Run dbt transformations
cd dbt_project
dbt run
dbt test

# 5. Start FastAPI server
uvicorn api.main:app --reload --host 0.0 --port 8000```

#### Option B: Dagster Orchestration (Recommended)
```bash
# Start Dagster UI
dagster dev

# Access Dagster UI at http://localhost:300
# - Navigate to Workspace" → ethiomed_pipeline"
# - Click "Launch Run" to execute the complete pipeline
# - Monitor execution in real-time
# - Set up daily schedule for automated runs
```

## 📊 API Usage

### Access the API
- **Interactive Documentation:** [http://localhost:8000](http://localhost:8000/docs)
- **Alternative Docs:** [http://localhost:80](http://localhost:800edoc)

### Key Endpoints

#### Health & Status
```bash
GET /api/health
# Returns pipeline health status
```

#### Business Analytics
```bash
# Top products by mention frequency
GET /api/reports/top-products?limit=10

# Channel activity analysis
GET /api/channels/{channel_name}/activity

# Message search with filters
GET /api/search/messages?query=vitamin&limit=20&date_from=2024-1# Data Exploration
```bash
# Get detection statistics
GET /api/detections/stats

# Search by detected objects
GET /api/detections/search?object=medicine&confidence=0.7
```

## 🔄 Pipeline Architecture

```mermaid
flowchart TD
    ATelegram Channels] -->|Telethon Scraper| B[Raw JSON Files<br/>data/raw/telegram_messages/]
    B -->|Python ETL| C[PostgreSQL<br/>raw_telegram_messages]
    C -->|dbt Staging| D[stg_telegram_messages]
    C -->|YOLO Detection| E[image_detections]
    D -->|dbt Marts| F[fct_messages]
    E -->|dbt Integration| G[fct_enriched_messages]
    F -->|FastAPI| H[Analytical API]
    G -->|FastAPI| H
    
    I[Dagster Orchestration] -->|Schedule & Monitor| A
    I -->|Coordinate| B
    I -->|Manage| C
    I -->|Execute| E
    I -->|Run| F
    I -->|Deploy| H
```

## 🛠️ Technology Stack

- **Data Ingestion:** Telethon (Telegram API)
- **Data Storage:** PostgreSQL
- **Data Processing:** Python, pandas
- **Data Modeling:** dbt (data build tool)
- **ML Enrichment:** YOLOv8 (object detection)
- **API Framework:** FastAPI
- **Orchestration:** Dagster
- **Containerization:** Docker & Docker Compose
- **Monitoring:** Dagster UI, application logs

## 📈 Data Models

### Raw Data
- `raw_telegram_messages`: Raw scraped messages with metadata
- `image_detections`: YOLO detection results with confidence scores

### Staging Models
- `stg_telegram_messages`: Cleaned and standardized message data
- `stg_image_detections`: Processed detection data

### Mart Models
- `fct_messages`: Fact table with message metrics
- `fct_enriched_messages`: Messages enriched with detection data

## 🔧 Configuration

### Environment Variables
```bash
# Telegram Configuration
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=your_phone_number

# Database Configuration
POSTGRES_URI=postgresql://user:password@host:port/database

# Pipeline Configuration
CHANNEL_NAMES=channel1,channel2,channel3
SCRAPE_LIMIT=100TECTION_CONFIDENCE=0.5
```

### dbt Configuration
- Profile: `dbt_project/profiles.yml`
- Models: `dbt_project/models/`
- Tests: Built-in data quality tests

## 📊 Monitoring & Observability

### Dagster UI
- Real-time pipeline monitoring
- Execution history and logs
- Error tracking and debugging
- Schedule management

### Application Logs
- Scraping logs: `logs/scrape_telegram.log`
- Docker logs: `docker-compose logs -f`
- API logs: Available in FastAPI docs

## 🚨 Troubleshooting

### Common Issues
1. **Telegram Authentication:** Ensure API credentials are correct
2. **Database Connection:** Verify PostgreSQL is running and accessible
3. **YOLO Dependencies:** Check CUDA/GPU requirements for detection
4**Docker Issues:** Restart containers with `docker-compose down && docker-compose up -d`

### Debug Commands
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f [service_name]

# Test database connection
docker-compose exec app python -c from api.database import engine; print(engine.execute('SELECT 1).fetchone())

# Test Telegram connection
python etl/test_telegram_connection.py
```

## 🔮 Future Enhancements

- [ ] Real-time streaming with Apache Kafka
- [ ] Advanced analytics with Apache Superset
- [ ] Machine learning model deployment
- i-language support for Ethiopian languages
-anced data quality monitoring
- [ ] Cost optimization and performance tuning

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

## 📞 Support

For questions, issues, or contributions, please contact the project maintainer or create an issue in the repository. 