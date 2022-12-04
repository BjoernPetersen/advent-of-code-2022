from pathlib import Path
from typing import Iterable

from more_itertools import chunked

from aoc.spi import Day
from aoc.spi import Task


def priority(item: str) -> int:
    base = 1 if item.islower() else 27
    return "abcdefghijklmnopqrstuvwxyz".index(item.lower()) + base


class Task1(Task):
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> int:
        rucksacks: list[tuple[str, str]] = [
            (line[: len(line) // 2], line[-len(line) // 2 :]) for line in input_lines
        ]
        return sum(
            priority(item)
            for r in rucksacks
            for item in set.intersection(set(r[0]), set(r[1]))
        )


class Task2(Task):
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> str | int:
        result = 0
        for chunk in chunked(input_lines, 3):
            intersection = set.intersection(*(set(r) for r in chunk))
            if len(intersection) != 1:
                raise ValueError

            result += priority(intersection.pop())

        return result


day = Day([Task1(), Task2()])
