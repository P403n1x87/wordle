import pytest
from wordle import Wordle, unix_words


@pytest.fixture
def wordle():
    yield Wordle("hello", unix_words())
