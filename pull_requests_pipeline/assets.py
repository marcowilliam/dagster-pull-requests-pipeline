from dagster import asset, RetryPolicy, ResourceParam
from github import Github
import pull_request_etl
from pull_requests_pipeline.config import RuntimeConfig


@asset(retry_policy=RetryPolicy(max_retries=5, delay=5))
def extract(github_api: ResourceParam[Github], config: RuntimeConfig):
    return pull_request_etl.extract(github_api, config.repo_name, config.pulls_count)


@asset(io_manager_key="pull_requests_io_manager")
def transform(extract):
    return pull_request_etl.transform(extract)


@asset
def report(context, github_api: ResourceParam[Github], transform):
    report_url = pull_request_etl.report(github_api, transform)
    context.log.info(report_url)
    return report_url