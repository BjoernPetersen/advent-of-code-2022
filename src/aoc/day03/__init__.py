from pathlib import Path
from typing import Iterable

from aoc.spi import Day
from aoc.spi import Task


class Task1(Task):
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> int:
        print("not implemented")
        return 0


day = Day([Task1()])
