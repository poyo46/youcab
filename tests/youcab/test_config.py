import pytest

from youcab.config import _mecab_config_dicdir, get_dicdirs
from youcab.errors import MecabConfigError


class TestMecabConfig:
    def test_should_return_a_directory_path(self):
        path = _mecab_config_dicdir()
        assert path.is_dir()

    def test_should_raise_an_error_when_the_executable_path_is_invalid(self):
        with pytest.raises(MecabConfigError):
            _mecab_config_dicdir(mecab_config_path="foobar")


class TestDicdirs:
    def test_should_return_a_list_of_directory_path(self):
        for dicdir in get_dicdirs():
            assert dicdir.is_dir()
