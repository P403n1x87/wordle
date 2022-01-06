import pytest
from wordle import Wordle, unix_words


@pytest.fixture
def wordle():
    words = {_ for _ in unix_words() if len(_) == 5}
    yield Wordle(next(iter(words)), words)
