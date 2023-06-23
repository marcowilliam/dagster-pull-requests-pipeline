from dagster import (
    Definitions,
    load_assets_from_modules,
    define_asset_job,
    ScheduleDefinition
)

from . import assets
from pull_requests_pipeline.io import PullRequestsIOManager
import os
from github import Github

all_assets = load_assets_from_modules([assets])
etl_job = define_asset_job(name="etl_job", selection="*")

defs = Definitions(
    assets=all_assets,
    jobs=[etl_job],
    resources={
        "pull_requests_io_manager": PullRequestsIOManager(),
        "github_api": Github(os.environ["GITHUB_ACCESS_TOKEN"])
    },
    schedules=[
        ScheduleDefinition(
            job=etl_job,
            cron_schedule="@daily",
        )
    ],
)
