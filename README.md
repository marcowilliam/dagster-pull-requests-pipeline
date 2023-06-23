# Dagster Pull Requests Pipeline
A dagster project that shows how to orchestrate an ETL python script using Dagster.

The pipeline gets the name of the Github repo the amount of pull requests to be analysed and creates a chart showing the amount of **changed files** in a PR by the **time in review** in hours as a Github Gist. This was done to have insights whether a specific project PR review process is impacted by smaller PRs or not.

Full development of the project can be found at https://codeline.blog

Example of the final result using github repo "dagster/dagster-io" with the last 30 pull requests.
<img width="974" alt="Screenshot 2023-06-23 at 09 58 57" src="https://github.com/marcowilliam/dagster-pull-requests-pipeline/assets/3015399/5c2408c8-64e1-4178-ba00-36d2f68cc94e">
