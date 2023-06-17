from dagster import asset
from pull_request import extract, transform, load, report
import markdown

ACCESS_TOKEN = "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"


@asset
def pull_requests_source_data():
    return extract("radar-parlamentar/radar")


@asset
def pull_requests_review_time(context, pull_requests_source_data):
    link = transform(pull_requests_source_data)
    context.log.info(link)
    return link


@asset
def load_into_file(context, pull_requests_review_time):
    context.log.info(load(pull_requests_review_time))


@asset
def report_to_gist(context):
    with open('output.md', 'r') as f:
        file = f.read()
        md_file = markdown.markdown(file)
        report_url = report(md_file)
        context.log.info(report_url)
        return report_url