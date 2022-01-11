import pytest
from wordle import TileColor, Wordle


def test_len_mismatch(wordle):
    with pytest.raises(AssertionError):
        wordle.submit("helloz")


def test_word_not_in_dict(wordle):
    with pytest.raises(AssertionError):
        wordle.submit("heloz")


def test_submit():
    wordle = Wordle("frogs", {"frogs", "broom"})
    assert wordle.submit("broom") == [TileColor(_) for _ in (0, 2, 2, 0, 0)]
