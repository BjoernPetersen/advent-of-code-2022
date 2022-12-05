from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from aoc.spi import Day
from aoc.spi import Task

move_pattern = re.compile(r"move (\d+) from (\d+) to (\d+)")

Buckets = list[list[str]]


@dataclass
class Move:
    source: int
    target: int
    amount: int

    def apply(self, buckets: Buckets):
        for _ in range(self.amount):
            item = buckets[self.source - 1].pop()
            buckets[self.target - 1].append(item)

    def apply9001(self, buckets: Buckets):
        items = buckets[self.source - 1][-self.amount :]
        buckets[self.source - 1] = buckets[self.source - 1][: -self.amount]
        buckets[self.target - 1].extend(items)

    @classmethod
    def decode(cls, line: str) -> Move:
        match = move_pattern.fullmatch(line)
        if not match:
            raise ValueError
        return cls(
            amount=int(match.group(1)),
            source=int(match.group(2)),
            target=int(match.group(3)),
        )

    def __repr__(self):
        return f"move {self.amount} from {self.source} to {self.target}"


def create_buckets(bucket_lines: list[str]) -> Buckets:
    # Is this function pretty? No. Does it work? Absolutely.
    number_row = bucket_lines[-1]
    bucket_count = (len(number_row) + 2) // 4
    buckets: Buckets = [[] for _ in range(bucket_count)]
    for line in bucket_lines[-2::-1]:
        for index in range(bucket_count):
            try:
                item = line[1 + (index * 4)]
            except IndexError:
                break

            if item.strip():
                buckets[index].append(item)
    return buckets


def decode(input_lines: Iterable[str]) -> tuple[Buckets, list[Move]]:
    bucket_lines: list[str] = []
    iterator = iter(input_lines)
    for line in iterator:
        if not line:
            break

        bucket_lines.append(line)

    moves = [Move.decode(line) for line in iterator]
    return create_buckets(bucket_lines), moves


class Task1(Task):
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> str:
        buckets, moves = decode(input_lines)
        for move in moves:
            move.apply(buckets)

        return "".join(stack[-1] for stack in buckets)


class Task2(Task):
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> str:
        buckets, moves = decode(input_lines)
        for move in moves:
            move.apply9001(buckets)

        return "".join(stack[-1] for stack in buckets)


day = Day([Task1(), Task2()])
