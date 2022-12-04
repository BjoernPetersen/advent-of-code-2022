from pathlib import Path
from typing import Callable, TypeAlias, Iterable

from aoc.spi import Task
from .common import Move, score_round, Round

Strategy: TypeAlias = list[Round]


def load_strategy(
    input_lines: Iterable[str], map_to_move: Callable[[str], Move]
) -> Strategy:
    result: Strategy = []
    for line in input_lines:
        parts = line.strip().split()
        moves = Round(
            their_move=map_to_move(parts[0]),
            my_move=map_to_move(parts[1]),
        )
        result.append(moves)

    return result


class Task1(Task):
    def map_to_move(self, code: str) -> Move:
        if code in ["A", "X"]:
            return Move.rock

        if code in ["B", "Y"]:
            return Move.paper

        if code in ["C", "Z"]:
            return Move.scissors

        raise ValueError(f"Unknown code: {code}")

    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> int:
        strategy = load_strategy(input_lines, self.map_to_move)
        return sum(score_round(it) for it in strategy)
