from dagster import Config


class RuntimeConfig(Config):
    pulls_count: int
    repo_name: str
