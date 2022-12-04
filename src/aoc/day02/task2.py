from __future__ import annotations

from enum import IntEnum
from pathlib import Path
from typing import TypeAlias

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


def load_strategy(input_path: Path) -> Strategy:
    result: Strategy = []
    with open(input_path) as f:
        for line in f.readlines():
            parts = line.strip().split()
            moves = map_to_move(parts[0]), map_to_outcome(parts[1])
            result.append(moves)

    return result


def make_round(move: Move, outcome: Outcome) -> Round:
    my_move: Move = move + outcome
    if my_move < min(Move):
        my_move = max(Move)
    elif my_move > max(Move):
        my_move = min(Move)

    return Round(move, my_move)


class Task2(Task):
    def run(self, input_file: Path, working_dir: Path) -> int:
        strategy = load_strategy(input_file)
        return sum(score_round(make_round(*it)) for it in strategy)
