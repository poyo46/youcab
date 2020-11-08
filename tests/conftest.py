from pathlib import Path

import pytest


def pytest_addoption(parser):
    # https://docs.pytest.org/en/latest/example/simple.html#pass-different-values-to-a-test-function-depending-on-command-line-options
    parser.addoption(
        "--dicdirs",
        required=True,
        action="append",
        default=[],
        help="MeCab ``dicdir`` paths.",
    )


@pytest.fixture(scope="session")
def dicdirs(request):
    dicdirs = request.config.getoption("--dicdirs")
    if len(dicdirs) == 0 or dicdirs == [""]:
        raise ValueError("One or more ``dicdirs`` must be specified.")
    return [None] + dicdirs


@pytest.fixture(scope="session")
def root_dir():
    return Path(__file__).parents[1].resolve()
