# Wordle

A simple, pure Python [Wordle](https://www.powerlanguage.co.uk/wordle/)
implementation.



## How to play

Install from GitHub using `pip`/`pipx` and run with `wordle`

~~~console
pipx install git+https://github.com/p403n1x87/wordle.git
wordle
~~~

> NOTE: This requires the file `/usr/share/dict/words/` to be present on your
> system to work. Most Linux systems have this file. If you want to play on
> Windows you can try installing via WSL.

<p align="center"><img src="art/wordle.gif"/></p>


## Wordle solver

The module contains a `WordleSolver` class that can be used to solve a Wordle.
See the tests for more details.
