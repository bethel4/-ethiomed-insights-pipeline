from dagster import ScheduleDefinition, DefaultScheduleStatus
from ..jobs.ethiomed_pipeline import ethiomed_pipeline_job

daily_ethiomed_schedule = ScheduleDefinition(
    job=ethiomed_pipeline_job,
    cron_schedule="0 6 * * *",  # Every day at 6 AM UTC
    name="daily_ethiomed_schedule",
    description="Run the Ethiomed pipeline daily at 6 AM UTC",
    default_status=DefaultScheduleStatus.STOPPED  # Start stopped, enable manually
) 