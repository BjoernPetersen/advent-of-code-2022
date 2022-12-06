from __future__ import annotations

from pathlib import Path
from typing import Iterable

from more_itertools import sliding_window

from aoc.spi import Day
from aoc.spi import Task


def find_start_marker(signals: str, marker_size: int) -> int:
    for window_number, window in enumerate(sliding_window(signals, marker_size)):
        if len(set(window)) == marker_size:
            return window_number + marker_size

    raise ValueError("No signal")


class Task1(Task):
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> str | int:
        return find_start_marker(list(input_lines)[0], marker_size=4)


class Task2(Task):
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> str | int:
        return find_start_marker(list(input_lines)[0], marker_size=14)


day = Day([Task1(), Task2()])
