#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="peter-tweets",
    version="1.0.0",
    description="Peter Steinberger's Twitter Wisdom Harvester - Parallel Agent Architecture",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "tweepy>=4.14.0",
        "click>=8.0",
        "rich>=13.0",
        "schedule>=1.2.0",
        "sqlite-utils>=3.0",
        "python-dotenv>=1.0.0",
        "backoff>=2.2.0",
        "httpx>=0.25.0",
    ],
    entry_points={
        "console_scripts": [
            "peter-tweets=peter_tweets.cli:main",
        ],
    },
    python_requires=">=3.8",
)