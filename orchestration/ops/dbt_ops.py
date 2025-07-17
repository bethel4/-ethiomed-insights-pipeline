import os
import subprocess
from dagster import op
from typing import Dict

@op(description="Run dbt transformations")
def run_dbt_transformations(context, yolo_result: Dict) -> Dict:
    if yolo_result.get("status") != "success":
        context.log.warning("Skipping dbt transformations due to YOLO detection failure")
        return {
            "status": "skipped",
            "message": "Skipped due to YOLO detection failure"
        }
    try:
        dbt_dir = os.path.join(os.getcwd(), "dbt_project")
        result = subprocess.run(
            ["dbt", "run"],
            capture_output=True,
            text=True,
            cwd=dbt_dir
        )
        if result.returncode == 0:
            context.log.info("dbt transformations completed successfully")
            test_result = subprocess.run(
                ["dbt", "test"],
                capture_output=True,
                text=True,
                cwd=dbt_dir
            )
            if test_result.returncode == 0:
                context.log.info("dbt tests passed successfully")
                return {
                    "status": "success",
                    "message": "dbt transformations and tests completed successfully",
                    "output": result.stdout + "\n" + test_result.stdout
                }
            else:
                context.log.warning(f"dbt tests failed: {test_result.stderr}")
                return {
                    "status": "warning",
                    "message": f"dbt transformations completed but tests failed: {test_result.stderr}",
                    "output": result.stdout
                }
        else:
            context.log.error(f"dbt transformations failed: {result.stderr}")
            return {
                "status": "error",
                "message": f"dbt transformations failed: {result.stderr}"
            }
    except Exception as e:
        context.log.error(f"Error in dbt transformations: {str(e)}")
        return {
            "status": "error",
            "message": f"Error in dbt transformations: {str(e)}"
        } 