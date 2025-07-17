from dagster import repository
from .jobs.ethiomed_pipeline import ethiomed_pipeline_job
from .schedules.daily_schedule import daily_ethiomed_schedule

@repository
def ethiomed_repository():
    return [
        ethiomed_pipeline_job,
        daily_ethiomed_schedule
    ] 