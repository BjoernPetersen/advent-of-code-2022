from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import portion
from portion import Interval

from aoc.spi import Day
from aoc.spi import Task


@dataclass
class Range:
    start: int
    end: int

    @classmethod
    def decode(cls, code: str) -> Range:
        return cls(*(int(it) for it in code.split("-")))

    def as_interval(self) -> Interval:
        return portion.closed(self.start, self.end)


class Task1(Task):
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> int:
        result = 0
        for line in input_lines:
            intervals = [Range.decode(code).as_interval() for code in line.split(",")]
            intersection = Interval.intersection(*intervals)
            if intersection in intervals:
                result += 1

        return result


class Task2(Task):
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> str | int:
        result = 0
        for line in input_lines:
            a, b = (Range.decode(code).as_interval() for code in line.split(","))
            if a.overlaps(b):
                result += 1

        return result


day = Day([Task1(), Task2()])
