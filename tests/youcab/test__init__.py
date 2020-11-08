from datetime import date
from typing import Dict

import pytest
import toml

import youcab


@pytest.fixture(scope="module")
def tool_poetry(root_dir) -> Dict:
    with open(root_dir / "pyproject.toml") as f:
        parsed_toml = toml.loads(f.read())
        return parsed_toml["tool"]["poetry"]


class TestPackage:
    def test_title(self, tool_poetry):
        assert youcab.__title__ == tool_poetry["name"]

    def test_description(self, tool_poetry):
        assert youcab.__description__ == tool_poetry["description"]

    def test_url(self, tool_poetry):
        assert youcab.__url__ == tool_poetry["homepage"]

    def test_version(self, tool_poetry):
        assert youcab.__version__ == tool_poetry["version"]

    def test_author(self, tool_poetry):
        assert youcab.__author__ in "".join(tool_poetry["authors"])

    def test_author_email(self, tool_poetry):
        assert youcab.__author_email__ in "".join(tool_poetry["authors"])

    def test_license(self, tool_poetry):
        assert youcab.__license__ == tool_poetry["license"]

    def test_copyright(self):
        year = date.today().year
        author = youcab.__author__
        assert youcab.__copyright__ == f"Copyright {year} {author}"
