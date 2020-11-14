import os
from typing import Callable, List, Optional

import pytest

from youcab import youcab
from youcab.errors import InvalidTokenizerError, NotFoundNodeFormatError
from youcab.word import Word


@pytest.mark.parametrize(
    "node_format",
    [None, r"%m\\n"],
)
@pytest.mark.parametrize(
    "unk_format",
    [None, r"%m\\n"],
)
def test__mecab_tagger(dicdirs, node_format, unk_format):
    tokens = ["毎日", "とても", "歩き", "ます"]
    text = "".join(tokens)
    for dicdir in dicdirs:
        tagger = youcab._mecab_tagger(
            dicdir=dicdir, node_format=node_format, unk_format=unk_format
        )
        result = tagger.parse(text)
        for token in tokens:
            assert token in result


def test__mecab_tagger_env_vars_should_be_available(dicdirs):
    os.environ["MECAB_DICDIR"] = dicdirs[-1]
    tagger = youcab._mecab_tagger(node_format=r"%m\\n")
    result = tagger.parse("こんにちは")
    assert result is not None


@pytest.mark.parametrize(
    "items, equal_to, include, expect",
    [
        (["aaa", "bbb", "ccc"], "bbb", None, 1),
        (["aaa", "bbb", "ccc"], "cc", None, None),
        (["aaa", "bbb", "ccc"], "ddd", None, None),
        (["aaa", "bbb", "ccc"], None, "ccc", 2),
        (["aaa", "bbb", "ccc"], None, "cc", 2),
        (["aaa", "bbb", "ccc"], None, "ddd", None),
    ],
)
def test__find_index(items, equal_to, include, expect):
    assert youcab._find_index(items, equal_to=equal_to, include=include) == expect


def test__auto_node_format(dicdirs):
    for dicdir in dicdirs:
        node_format = youcab._auto_node_format(dicdir=dicdir)
        assert len(node_format) > 0


def test__auto_node_format_if_not_found(monkeypatch):
    def find_index(
        items: List[str], equal_to: Optional[str] = None, include: Optional[str] = None
    ):
        return None

    monkeypatch.setattr(youcab, "_find_index", find_index)
    with pytest.raises(NotFoundNodeFormatError):
        youcab._auto_node_format()


@pytest.mark.parametrize(
    "tokenize",
    [
        lambda x: [
            Word("楽しい", ["形容詞", "一般"], base="楽しい", c_type="形容詞", c_form="連体形-一般"),
            Word("本", ["名詞", "普通名詞", "一般"]),
            Word("を", ["助詞", "格助詞"]),
            Word("よく", ["副詞"]),
            Word("読み", ["動詞", "一般"], base="読む", c_type="五段-マ行", c_form="連用形-一般"),
            Word("ます", ["助動詞"], base="ます", c_type="助動詞-マス", c_form="終止形-一般"),
        ]
    ],
)
def test__check_tokenizer_returns_none_if_valid(tokenize):
    assert youcab._check_tokenizer(tokenize) is None


@pytest.mark.parametrize(
    "tokenize",
    [
        lambda x: [],  # invalid length
        lambda x: [
            Word("楽しい", ["形容詞", "一般"], base="楽しい", c_type="形容詞", c_form="連体形-一般"),
            Word("本", ["名詞", "普通名詞", "一般"]),
            Word("を", ["助詞", "格助詞"]),
            Word("良く", ["副詞"]),  # invalid surface
            Word("読み", ["動詞", "一般"], base="読む", c_type="五段-マ行", c_form="連用形-一般"),
            Word("ます", ["助動詞"], base="ます", c_type="助動詞-マス", c_form="終止形-一般"),
        ],
        lambda x: [
            Word("楽しい", ["形容詞", "一般"], base="楽しい", c_type="形容詞", c_form="連体形-一般"),
            Word("本", ["noun"]),  # invalid pos
            Word("を", ["助詞", "格助詞"]),
            Word("よく", ["副詞"]),
            Word("読み", ["動詞", "一般"], base="読む", c_type="五段-マ行", c_form="連用形-一般"),
            Word("ます", ["助動詞"], base="ます", c_type="助動詞-マス", c_form="終止形-一般"),
        ],
        lambda x: [
            Word("楽しい", ["形容詞", "一般"], base="楽しい", c_type="形容詞", c_form="連体形-一般"),
            Word("本", ["名詞", "普通名詞", "一般"]),
            Word("を", ["助詞", "格助詞"]),
            Word("よく", ["副詞"], base=""),  # invalid base
            Word("読み", ["動詞", "一般"], base="読む", c_type="五段-マ行", c_form="連用形-一般"),
            Word("ます", ["助動詞"], base="ます", c_type="助動詞-マス", c_form="終止形-一般"),
        ],
        lambda x: [
            Word("楽しい", ["形容詞", "一般"], base="楽しい", c_type="形容詞", c_form="連体形-一般"),
            Word("本", ["名詞", "普通名詞", "一般"]),
            Word("を", ["助詞", "格助詞"], c_type="X", c_form="Y"),  # invalid conjugation
            Word("よく", ["副詞"]),
            Word("読み", ["動詞", "一般"], base="読む", c_type="五段-マ行", c_form="連用形-一般"),
            Word("ます", ["助動詞"], base="ます", c_type="助動詞-マス", c_form="終止形-一般"),
        ],
    ],
)
def test__check_tokenizer_raises_error_if_invalid(tokenize):
    with pytest.raises(InvalidTokenizerError):
        youcab._check_tokenizer(tokenize)


def test_can_generate_tokenizer(dicdirs):
    for dicdir in dicdirs:
        print("dicdir = " + str(dicdir))
        youcab.generate_tokenizer(dicdir=dicdir)


def test_generate_tokenizer_raises_error_if_node_format_is_invalid(dicdirs):
    with pytest.raises(InvalidTokenizerError):
        youcab.generate_tokenizer(dicdir=dicdirs[0], node_format=r"%m%H\\n")


def test_generated_tokenizer_returns_unknown_token_as_noun(monkeypatch):
    def auto_node_format(dicdir: Optional[str] = None):
        return ""

    def mecab_tagger(
        dicdir: Optional[str] = None,
        node_format: Optional[str] = None,
        unk_format: Optional[str] = None,
    ):
        class MecabTagger:
            def parse(self, text):
                return None

        tagger = MecabTagger()
        return tagger

    def check_tokenizer(tokenize: Callable[[str], List[Word]]) -> None:
        return None

    monkeypatch.setattr(youcab, "_auto_node_format", auto_node_format)
    monkeypatch.setattr(youcab, "_mecab_tagger", mecab_tagger)
    monkeypatch.setattr(youcab, "_check_tokenizer", check_tokenizer)

    tokenize = youcab.generate_tokenizer()
    text = "これは未知語です！"
    words = tokenize(text)
    assert len(words) == 1
    assert words[0].surface == text
    assert words[0].pos == ["名詞"]
