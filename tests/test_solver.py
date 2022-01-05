from wordle import TileColor, WordleSolver
from wordle.words import WORDS


def diagnose(wordle, ws, guess, words):
    ws.words = words
    ws.shrink(guess, wordle.submit(guess))


def test_solver(wordle):
    success = 0
    for runs in range(200):
        ws = WordleSolver(list(WORDS))
        guesses = []
        for a in range(10):
            try:
                guess = ws.guess()
            except Exception:
                for guess, words in guesses:
                    print(guess, words)
                diagnose(wordle, ws, *guesses[-2])
                raise
            outcome = wordle.submit(guess)
            if set(outcome) == {TileColor.GREEN}:
                break
            ws.shrink(guess, outcome)
            guesses.append((guess, ws.words))
        else:
            raise RuntimeError("I couldn't solve the Wordle :(")

        assert guess == wordle.secret, "guess is correct"

        success += a < 6

    assert success / runs > 0.95
