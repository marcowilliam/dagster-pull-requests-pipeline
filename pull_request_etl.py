from github import Github, InputFileContent
import pandas as pd
import pickle
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import jupytext
from dagster import get_dagster_logger


logger = get_dagster_logger()


def extract(github_api, repo_name, pulls_count):
    repo = github_api.get_repo(repo_name)
    closed_pulls = list(repo.get_pulls(state="closed").reversed[:pulls_count])
    closed_pulls_details = [
        repo.get_pull(number=pull.number) for pull in closed_pulls
    ]
    return closed_pulls_details


def transform(pulls):
    df = pd.DataFrame(
        [
            {
                "changed_files": pull.changed_files,
                "created_at": pull.created_at,
                "merged_at": pull.merged_at,
                "time_in_review": (
                    round((pull.merged_at - pull.created_at).total_seconds() / 3600, 1)
                    if pull.created_at is not None and pull.merged_at is not None else 0
                )
            }
            for pull in pulls
        ]
    )
    df = df[df.time_in_review != 0].sort_values(by="time_in_review")

    logger.info(df)

    md_content = f"""
# Github Pull Requests Review Time

```python
import pickle
pull_requests = pickle.loads({pickle.dumps(df)!r})

## Repo pull requests with higher review time by changed files

pull_requests.reset_index().plot.bar(x="time_in_review", y="changed_files")

    """

    return md_content


def load(md_content):
    with open("output.md", "w") as f:
        f.write(md_content)


def report(github_api, md_file):
    nb = jupytext.reads(md_file, "md")
    ExecutePreprocessor().preprocess(nb)
    notebook_visualization = nbformat.writes(nb)
    gist = (
        github_api
        .get_user()
        .create_gist(
            public=False,
            files={
                "pull_requests_analyses.ipynb": InputFileContent(notebook_visualization),
            },
        )
    )
    return gist.html_url

ACCESS_TOKEN = "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"
github_api = Github(ACCESS_TOKEN)

if __name__ == "__main__":
    # Run ETL
    input = extract(github_api, "dagster-io/dagster", 30)
    output = transform(input)
    load(output)

    # Run report
    with open('output.md', 'r') as f:
        file = f.read()
        report_url = report(github_api, file)
        print(report_url)
