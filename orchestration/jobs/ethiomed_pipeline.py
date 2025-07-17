from dagster import graph
from ..ops.telegram_ops import scrape_telegram_data
from ..ops.postgres_ops import load_to_postgres
from ..ops.yolo_ops import run_yolo_detection
from ..ops.dbt_ops import run_dbt_transformations

@graph(description="Complete Ethiomed data pipeline")
def ethiomed_pipeline_graph():
    telegram_result = scrape_telegram_data()
    postgres_result = load_to_postgres(telegram_result)
    yolo_result = run_yolo_detection(postgres_result)
    dbt_result = run_dbt_transformations(yolo_result)
    return dbt_result

ethiomed_pipeline_job = ethiomed_pipeline_graph.to_job(
    name="ethiomed_pipeline",
    description="Complete pipeline for Ethiomed data processing"
) 