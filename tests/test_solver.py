from wordle import TileColor, WordleSolver, unix_words


def test_solver(wordle):

    ws = WordleSolver([_ for _ in unix_words() if len(_) == 5])

    for i in range(6):
        guess = ws.guess()
        outcome = wordle.submit(guess)
        if set(outcome) == {TileColor.GREEN}:
            break
        ws.shrink(guess, outcome)
    else:
        raise RuntimeError("I couldn't solve the Wordle :(")

    assert guess == wordle.secret
