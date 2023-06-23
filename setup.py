from setuptools import find_packages, setup

setup(
    name="pull_requests_pipeline",
    packages=find_packages(exclude=["pull_requests_pipeline_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "PyGithub",
        "matplotlib",
        "pandas",
        "nbconvert",
        "nbformat",
        "ipykernel",
        "jupytext"
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
