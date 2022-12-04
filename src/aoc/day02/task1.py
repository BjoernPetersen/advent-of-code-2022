from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import TypeAlias, Callable

from aoc.spi import Task


class Move(IntEnum):
    rock = 1
    paper = 2
    scissors = 3


@dataclass(frozen=True)
class Round:
    their_move: Move
    my_move: Move


Strategy: TypeAlias = list[Round]


def load_strategy(input_path: Path, map_to_move: Callable[[str], Move]) -> Strategy:
    result: Strategy = []
    with open(input_path) as f:
        for line in f.readlines():
            parts = line.strip().split()
            moves = Round(
                their_move=map_to_move(parts[0]),
                my_move=map_to_move(parts[1]

                                    ),
            )
            result.append(moves)

    return result


def score_round(round: Round) -> int:
    outcome_points: int
    their_move = round.their_move
    my_move = round.my_move

    if their_move == my_move:
        # Draw
        outcome_points = 3
    elif their_move % len(Move) + 1 == my_move:
        # Win
        outcome_points = 6
    else:
        # Loss
        outcome_points = 0

    return outcome_points + my_move


class Task1(Task):
    def map_to_move(self, code: str) -> Move:
        if code in ["A", "X"]:
            return Move.rock

        if code in ["B", "Y"]:
            return Move.paper

        if code in ["C", "Z"]:
            return Move.scissors

        raise ValueError(f"Unknown code: {code}")

    def run(self, input_file: Path, working_dir: Path) -> int:
        strategy = load_strategy(input_file, self.map_to_move)
        return sum(score_round(it) for it in strategy)
