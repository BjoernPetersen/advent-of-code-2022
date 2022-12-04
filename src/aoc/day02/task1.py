from pathlib import Path
from typing import Callable, TypeAlias

from aoc.spi import Task
from .common import Move, score_round, Round

Strategy: TypeAlias = list[Round]


def load_strategy(input_path: Path, map_to_move: Callable[[str], Move]) -> Strategy:
    result: Strategy = []
    with open(input_path) as f:
        for line in f.readlines():
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

    def run(self, input_file: Path, working_dir: Path) -> int:
        strategy = load_strategy(input_file, self.map_to_move)
        return sum(score_round(it) for it in strategy)
