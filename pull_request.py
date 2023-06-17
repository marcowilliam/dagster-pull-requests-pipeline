from github import Github, InputFileContent
import pandas as pd
import pickle
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import jupytext
from dagster import get_dagster_logger

ACCESS_TOKEN = "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"
logger = get_dagster_logger()


def extract(repo_name):
    repo = Github(ACCESS_TOKEN).get_repo(repo_name)
    closed_pulls = list(repo.get_pulls(state="closed"))
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
                "time_in_review": round((pull.merged_at - pull.created_at).total_seconds() / 3600,
                                        1) if pull.created_at is not None and pull.merged_at is not None else 0
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

    ## Repo 30 pull requests with higher review time by changed files

    pull_requests.tail(30).reset_index().plot.bar(x="time_in_review", y="changed_files")

        """

    nb = jupytext.reads(md_content, "md")
    ExecutePreprocessor().preprocess(nb)

    return nbformat.writes(nb)


def load(md_content):
    gist = (
        Github(ACCESS_TOKEN)
        .get_user()
        .create_gist(
            public=False,
            files={
                "pull_requests_analyses.ipynb": InputFileContent(md_content),
            },
        )
    )

    print(gist.html_url)
    return gist.html_url
    # with open("output.md", "w") as f:
    #     f.write(md_content)
    #     return f


def report(md_file):
    nb = jupytext.reads(md_file, "md")
    ExecutePreprocessor().preprocess(nb)
    notebook_visualization = nbformat.writes(nb)
    gist = (
        Github(ACCESS_TOKEN)
        .get_user()
        .create_gist(
            public=False,
            files={
                "pull_requests_analyses.ipynb": InputFileContent(notebook_visualization),
            },
        )
    )
    return gist.html_url


if __name__ == "__main__":
    # Run ETL
    input = extract("radar-parlamentar/radar")
    output = transform(input)
    # load(output)
    #
    # # Run report
    # with open('output.md', 'r') as f:
    #     file = f.read()
    #     report_url = report(file)
    #     print(report_url)