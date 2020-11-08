import pytest

from youcab.word import Word


@pytest.fixture(scope="module")
def required_args():
    return {"surface": "日本", "pos": ["名詞", "固有名詞", "地名", "国"]}


@pytest.fixture(scope="module")
def full_args():
    return {
        "surface": "動け",
        "pos": ["動詞", "一般"],
        "base": "動く",
        "c_type": "五段-カ行",
        "c_form": "命令形",
    }


class TestWord:
    def test_can_init_with_only_required_args(self, required_args):
        word = Word(**required_args)
        assert word is not None

    def test_can_init_with_full_args(self, full_args):
        word = Word(**full_args)
        assert word is not None

    def test_default_value_of_base_is_the_same_as_surface(self, required_args):
        word = Word(**required_args)
        assert word.base == word.surface

    def test_both_c_type_and_c_form_are_required_if_necessary(self, full_args):
        word0 = Word(
            surface=full_args["surface"],
            pos=full_args["pos"],
            base=full_args["base"],
            c_type=full_args["c_type"],
        )
        assert word0.c_type == ""  # != full_args["c_type"]
        assert word0.c_form == ""

        word1 = Word(
            surface=full_args["surface"],
            pos=full_args["pos"],
            base=full_args["base"],
            c_form=full_args["c_form"],
        )
        assert word1.c_type == ""
        assert word1.c_form == ""  # != full_args["c_form"]

    def test_attributes(self, full_args):
        word = Word(**full_args)
        for attr in Word.ATTRS:
            assert getattr(word, attr) == full_args[attr]

    def test_to_dic(self, full_args):
        word = Word(**full_args)
        word_dict = word.to_dict()
        assert type(word_dict) == dict
        for attr in Word.ATTRS:
            assert word_dict[attr] == full_args[attr]

    def test_to_str(self, full_args):
        word = Word(**full_args)
        word_str = str(word)
        for key in Word.ATTRS:
            assert key in word_str
