from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable, NamedTuple

from aoc.spi import Day
from aoc.spi import Task


class Vector(NamedTuple):
    x: int
    y: int

    def __sub__(self, other) -> Vector:
        if not isinstance(other, Vector):
            raise ValueError("Unrelated types")

        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other) -> Vector:
        if not isinstance(other, Vector):
            raise ValueError("Unrelated types")

        return Vector(self.x + other.x, self.y + other.y)

    def __abs__(self):
        return Vector(abs(self.x), abs(self.y))

    def length(self) -> float:
        # Euclidian norm
        return math.sqrt(sum(x**2 for x in self))

    def unit(self) -> Vector:
        norm = self.length()
        x, x_remainder = divmod(self.x, norm)
        y, y_remainder = divmod(self.y, norm)
        if x_remainder or y_remainder:
            raise ValueError("Floating point vectors are not supported")

        return Vector(int(x), int(y))


def parse_move(line: str) -> Vector:
    direction, length_string = line.split()
    length = int(length_string)

    if direction == "R":
        return Vector(length, 0)

    if direction == "L":
        return Vector(-length, 0)

    if direction == "U":
        return Vector(0, length)

    if direction == "D":
        return Vector(0, -length)

    raise ValueError(f"Unknown move direction: {direction}")


def get_steps(move: Vector) -> Iterable[Vector]:
    length = int(move.length())
    if length == 1:
        yield move
    else:
        unit = move.unit()
        for _ in range(length):
            yield unit


def follow_head(head: Vector, tail: Vector) -> Vector:
    if head == tail:
        return tail

    diff = head - tail
    if diff.length() < 2:
        return tail

    move = Vector(
        x=max(-1, min(1, diff.x)),
        y=max(-1, min(1, diff.y)),
    )
    return tail + move


class Task1(Task):
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> str | int:
        start_position = Vector(0, 0)
        positions = {start_position}
        head = start_position
        tail = start_position
        for line in input_lines:
            move = parse_move(line)
            for step in get_steps(move):
                head += step
                tail = follow_head(head=head, tail=tail)
                positions.add(tail)

        return len(positions)


class Task2(Task):
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> str | int:
        start_position = Vector(0, 0)
        positions = {start_position}
        head = start_position
        tails = [start_position] * 9
        for line in input_lines:
            move = parse_move(line)
            for step in get_steps(move):
                head += step
                leader = head
                for tail_index in range(len(tails)):
                    tail = tails[tail_index]
                    leader = follow_head(head=leader, tail=tail)
                    tails[tail_index] = leader

                    if tail_index == len(tails) - 1:
                        positions.add(leader)

        return len(positions)


day = Day([Task1(), Task2()])
