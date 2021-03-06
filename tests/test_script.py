from inspect import cleandoc
from unittest.mock import patch

import pytest

from emojisearcher.script import (clean_non_emoji_characters,
                                  get_matching_emojis,
                                  get_emojis_for_word,
                                  user_select_emoji)


@pytest.mark.parametrize("word, expected", [
    ("ð¤½\u200dâï¸'", "ð¤½"),
    ("12ð¤½34", "ð¤½"),
    ("abcð¤½Ã±=)", "ð¤½"),
])
def test_clean_non_emoji_characters(word, expected):
    assert clean_non_emoji_characters(word) == expected


@pytest.mark.parametrize("words, matches", [
    ("heart snake beer", ['ð', 'ð', 'ðº']),
    ("hand scream angry", ['ð', 'ð±', 'ð ']),
    ("struck dog", ['ð¤©', 'ð¶']),
    ("slee tree fire water cat", ['ð´', 'ð', 'ð¥', 'ð¤½', 'ð¸']),
])
def test_get_matching_emojis(words, matches):
    assert get_matching_emojis(words.split()) == matches


@pytest.mark.parametrize("word, num_results, emoji", [
    ("heart", 36, 'ð'),
    ("snake", 1, 'ð'),
    ("grin", 9, 'ðº'),
])
def test_get_emojis_for_word(word, num_results, emoji):
    result = get_emojis_for_word(word)
    assert len(result) == num_results
    assert result[0] == emoji


@patch("builtins.input", side_effect=['a', 10, 2, 'q'])
def test_user_selects_tree_emoji(mock_input, capfd):
    trees = ['ð', 'ð³', 'ð²', 'ð´', 'ð']
    ret = user_select_emoji(trees)
    assert ret == "ð³"
    actual = capfd.readouterr()[0].strip()
    expected = cleandoc("""
    1 ð
    2 ð³
    3 ð²
    4 ð´
    5 ð
    a is not an integer.
    1 ð
    2 ð³
    3 ð²
    4 ð´
    5 ð
    10 is not a valid option.
    1 ð
    2 ð³
    3 ð²
    4 ð´
    5 ð
    """)
    assert actual == expected
