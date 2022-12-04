from pathlib import Path

from aoc.spi import Day
from aoc.spi import Task


def read_inventories(input_file: Path) -> list[list[int]]:
    inventories: list[list[int]] = []
    current: list[int] = []

    with open(input_file) as f:
        for line in f.readlines():
            nude_line = line.strip()
            if nude_line:
                current.append(int(nude_line))
            else:
                inventories.append(current)
                current = []

    if current:
        inventories.append(current)

    return inventories


class Task1(Task):
    def run(self, input_file: Path, working_dir: Path) -> str:
        inventories = read_inventories(input_file)
        sums = [sum(inv) for inv in inventories]
        return str(max(sums))


class Task2(Task):
    def run(self, input_file: Path, working_dir: Path) -> str:
        inventories = read_inventories(input_file)
        sums = [sum(inv) for inv in inventories]
        sums.sort()
        return str(sum(sums[-3:]))


day = Day([Task1(), Task2()])
