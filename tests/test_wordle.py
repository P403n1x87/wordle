import pytest


def test_len_mismatch(wordle):
    with pytest.raises(AssertionError):
        wordle.submit("helloz")


def test_word_not_in_dict(wordle):
    with pytest.raises(AssertionError):
        wordle.submit("heloz")
