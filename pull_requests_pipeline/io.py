from dagster import IOManager
import pull_request_etl


class PullRequestsIOManager(IOManager):
    def load_input(self, context):
        with open("output.md", 'r') as f:
            return f.read()

    def handle_output(self, context, md_content) -> None:
        pull_request_etl.load(md_content)