import typing as _t
from collections import defaultdict
from enum import Enum
from random import choice

from wordle.words import WORDS


class TileColor(Enum):
    GRAY = 0
    YELLOW = 1
    GREEN = 2


class Wordle:
    def __init__(self, secret: str, words: _t.Iterator[str]) -> None:
        self.secret = secret.lower()
        self.words = {_ for _ in words if len(_) == len(secret)}

    def submit(self, word: str) -> _t.List[TileColor]:
        assert len(word) == len(self.secret), "word has same length as secret"
        assert word in self.words, "word is in the dictionary"

        ss = set(self.secret)
        hints = []
        for a, b in zip(word.lower(), self.secret):
            if a == b:
                hints.append(TileColor.GREEN)
            elif a in ss:
                hints.append(TileColor.YELLOW)
                ss.remove(a)
            else:
                hints.append(TileColor.GRAY)
        return hints


class WordleSolver:
    def __init__(self, words: _t.List[str]) -> None:
        self.words = words

        self.correct: _t.Dict[int, str] = {}
        self.misplaced: _t.Dict[int, _t.Set[str]] = defaultdict(set)
        self.include: _t.Set[str] = set()

    def guess(self) -> str:
        # TODO: Use entropy or other heuristics to make better guesses
        scored = [(len(set(_)), _) for _ in self.words]
        m = max(s for s, _ in scored)
        return choice([w for s, w in scored if s == m])

    def shrink(self, word: str, tiles: _t.List[TileColor]) -> None:
        exclude: _t.Set[str] = set()
        for i, (c, t) in enumerate(zip(word, tiles)):
            if t is TileColor.GRAY and c not in self.include:
                exclude.add(c)
            elif t is TileColor.GREEN:
                self.correct[i] = c
                self.include.add(c)
            else:
                self.misplaced[i].add(c)
                self.include.add(c)

        self.words = [
            word
            for word in self.words
            if not (
                exclude & set(word)
                or not all(word[i] == c for i, c in self.correct.items())
                or any(
                    word[i] in self.misplaced[i]
                    for i in range(len(word))
                    if i not in self.correct
                )
                or not (self.include <= set(word))
            )
        ]


def unix_words():
    return (
        _.lower()
        for _ in (_.strip() for _ in open("/usr/share/dict/words"))
        if all(c.isalpha() for c in _)
    )


def run():
    print("W O R D L E\n")

    w = Wordle(next(iter(WORDS)), WORDS)

    C = {TileColor.GREEN: 32, TileColor.YELLOW: 33, TileColor.GRAY: "38;5;244"}
    for i in range(6):
        while True:
            try:
                guess = input(".....\r").strip().lower()
            except KeyboardInterrupt:
                print("\n👋 Bye!")
                return
            if guess in WORDS:
                break
            print("\033[A", end="")

        outcome = w.submit(guess)
        print("\033[A", end="")
        print(
            "".join([f"\033[{C[t]}m{c.upper()}\033[0m" for c, t in zip(guess, outcome)])
        )
        if set(outcome) == {TileColor.GREEN}:
            print("✨ 🍰 ✨")
            return
    print("💀 GAME OVER 💀")


def solve():
    print("W O R D L E   S O L V E R\n")

    print(
        "Use \033[38;5;244;1m0\033[0m for \033[38;5;244mgray\033[0m,"
        " \033[33;1m1\033[0m for \033[33;1myellow\033[0m "
        "and \033[32;1m2\033[0m for \033[32;1mgreen\033[0m\n"
    )

    ws = WordleSolver(list(WORDS))

    try:
        guess = input("Your guess: ").strip().lower()
        if not guess:
            return
        for _ in range(6):
            outcome = input("The outcome: ").strip()
            if not outcome:
                return
            ws.shrink(guess, [TileColor(int(_)) for _ in outcome])
            guess = ws.guess()
            print(f"Try '{guess.upper()}'")
            print("\033[A\033[A" + " " * 32, end="\r")
    except KeyboardInterrupt:
        print()
    finally:
        print("\n👋 Bye!")


if __name__ == "__main__":
    run()
