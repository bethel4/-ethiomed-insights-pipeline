import os
import subprocess
from dagster import op
from typing import Dict

@op(description="Load scraped data into PostgreSQL")
def load_to_postgres(context, telegram_result: Dict) -> Dict:
    if telegram_result.get("status") != "success":
        context.log.warning("Skipping Postgres load due to Telegram scraping failure")
        return {
            "status": "skipped",
            "message": "Skipped due to Telegram scraping failure"
        }
    try:
        result = subprocess.run(
            ["python3", "etl/load_to_postgres.py"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        if result.returncode == 0:
            context.log.info("PostgreSQL loading completed successfully")
            return {
                "status": "success",
                "message": "Data loaded to PostgreSQL successfully",
                "output": result.stdout
            }
        else:
            context.log.error(f"PostgreSQL loading failed: {result.stderr}")
            return {
                "status": "error",
                "message": f"PostgreSQL loading failed: {result.stderr}"
            }
    except Exception as e:
        context.log.error(f"Error in PostgreSQL loading: {str(e)}")
        return {
            "status": "error",
            "message": f"Error in PostgreSQL loading: {str(e)}"
        } 