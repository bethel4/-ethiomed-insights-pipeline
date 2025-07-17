import os
import subprocess
from dagster import op
from typing import Dict

@op(description="Run YOLO object detection on scraped images")
def run_yolo_detection(context, postgres_result: Dict) -> Dict:
    if postgres_result.get("status") != "success":
        context.log.warning("Skipping YOLO detection due to Postgres loading failure")
        return {
            "status": "skipped",
            "message": "Skipped due to Postgres loading failure"
        }
    try:
        result = subprocess.run(
            ["python3", "etl/run_yolo_detection.py"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        if result.returncode == 0:
            context.log.info("YOLO detection completed successfully")
            return {
                "status": "success",
                "message": "YOLO detection completed successfully",
                "output": result.stdout
            }
        else:
            context.log.error(f"YOLO detection failed: {result.stderr}")
            return {
                "status": "error",
                "message": f"YOLO detection failed: {result.stderr}"
            }
    except Exception as e:
        context.log.error(f"Error in YOLO detection: {str(e)}")
        return {
            "status": "error",
            "message": f"Error in YOLO detection: {str(e)}"
        } 