from __future__ import annotations

from enum import IntEnum
from pathlib import Path
from typing import TypeAlias, Iterable

from aoc.spi import Task
from .common import Move, score_round, Round


class Outcome(IntEnum):
    lose = -1
    win = 1
    draw = 0


Strategy: TypeAlias = list[tuple[Move, Outcome]]


def map_to_move(code: str) -> Move:
    return {
        "A": Move.rock,
        "B": Move.paper,
        "C": Move.scissors,
    }[code]


def map_to_outcome(code: str) -> Outcome:
    return {
        "X": Outcome.lose,
        "Y": Outcome.draw,
        "Z": Outcome.win,
    }[code]


def load_strategy(input_lines: Iterable[str]) -> Strategy:
    result: Strategy = []
    for line in input_lines:
        parts = line.strip().split()
        moves = map_to_move(parts[0]), map_to_outcome(parts[1])
        result.append(moves)

    return result


def make_round(move: Move, outcome: Outcome) -> Round:
    my_move: Move = move + outcome  # type: ignore
    if my_move < min(Move):
        my_move = max(Move)
    elif my_move > max(Move):
        my_move = min(Move)

    return Round(move, my_move)


class Task2(Task):
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> int:
        strategy = load_strategy(input_lines)
        return sum(score_round(make_round(*it)) for it in strategy)
