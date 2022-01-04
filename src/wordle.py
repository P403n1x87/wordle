import typing as _t
from collections import defaultdict
from enum import Enum
from random import choice


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

        self.exclude: _t.Set[str] = set()
        self.correct: _t.Dict[int, str] = {}
        self.misplaced: _t.Dict[int, _t.Set[str]] = defaultdict(set)
        self.include: _t.Set[str] = set()

    def guess(self) -> str:
        return choice(self.words)

    def shrink(self, word: str, tiles: _t.List[TileColor]) -> None:
        for i, (c, t) in enumerate(zip(word, tiles)):
            if t is TileColor.GRAY:
                self.exclude.add(c)
            elif t is TileColor.GREEN:
                self.correct[i] = c
            else:
                self.misplaced[i].add(c)
                self.include.add(c)

        feasible = [
            (
                len(
                    {c for i, c in enumerate(word) if i not in self.correct}
                    & self.include
                ),
                word,
            )
            for word in self.words
            if not (
                self.exclude & set(word)
                or not all(word[i] == c for i, c in self.correct.items())
                or any(
                    word[i] in self.misplaced[i]
                    for i in range(len(word))
                    if i not in self.correct
                )
            )
        ]

        hi = max(s for s, _ in feasible)
        self.words = [w for s, w in feasible if s == hi]


def unix_words():
    return (
        _.lower()
        for _ in (_.strip() for _ in open("/usr/share/dict/words"))
        if all(c.isalpha() for c in _)
    )


def run():
    print("W O R D L E\n")
    words = {_ for _ in unix_words() if len(_) == 5}
    word = words.pop()
    words.add(word)
    w = Wordle(word, unix_words())

    C = {TileColor.GREEN: 32, TileColor.YELLOW: 33, TileColor.GRAY: "38;5;244"}
    for i in range(6):
        while True:
            guess = input(".....\r").strip().lower()
            if guess in words:
                break
            print("\033[A", end="")

        outcome = w.submit(guess)
        print(
            "\033[A"
            + "".join(
                [f"\033[{C[t]}m{c.upper()}\033[0m" for c, t in zip(guess, outcome)]
            )
        )
        if set(outcome) == {TileColor.GREEN}:
            print("✨ 🍰 ✨")
            break
    else:
        print("💀 GAME OVER 💀")


if __name__ == "__main__":
    run()
