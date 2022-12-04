from pathlib import Path
from typing import Iterable

from aoc.spi import Day
from aoc.spi import Task


def read_inventories(input_lines: Iterable[str]) -> list[list[int]]:
    inventories: list[list[int]] = []
    current: list[int] = []

    for line in input_lines:
        if line:
            current.append(int(line))
        else:
            inventories.append(current)
            current = []

    if current:
        inventories.append(current)

    return inventories


class Task1(Task):
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> int:
        inventories = read_inventories(input_lines)
        sums = [sum(inv) for inv in inventories]
        return max(sums)


class Task2(Task):
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> int:
        inventories = read_inventories(input_lines)
        sums = [sum(inv) for inv in inventories]
        sums.sort()
        return sum(sums[-3:])


day = Day([Task1(), Task2()])
