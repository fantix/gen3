#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "aiohttp",
    "edgedb",
    "jsonschema",
    "ruamel.yaml",
    "tartiflette",
    "tartiflette-aiohttp",
    "uvloop",
]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

setup(
    author="University of Chicago",
    author_email="cdis@uchicago.edu",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    description="Gen3 is how data commons are made.",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="gen3",
    name="gen3server",
    packages=find_packages(include=["gen3"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/uc-cdis/gen3",
    version="3.2.0",
    zip_safe=False,
    entry_points=dict(console_scripts=["gen3=gen3.cli:main"]),
)
