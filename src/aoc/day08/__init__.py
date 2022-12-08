from __future__ import annotations

import operator
from dataclasses import dataclass
from enum import IntEnum
from functools import reduce
from pathlib import Path
from typing import Iterable, NamedTuple

from aoc.spi import Day
from aoc.spi import Task


class Direction(IntEnum):
    ascending = 1
    descending = -1


class Position(NamedTuple):
    x: int
    y: int

    def __sub__(self, other) -> Position:
        if not isinstance(other, Position):
            raise ValueError(f"Not a position: {other}")
        return Position(self.x - other.x, self.y - other.y)

    def __len__(self) -> int:
        return abs(self.x) + abs(self.y)


@dataclass
class Tree:
    position: Position
    height: int


class Grid:
    def __init__(self, trees: list[list[Tree]]):
        self._trees = trees
        self.height = len(trees)
        self.width = len(trees[0])

    def get_tree(self, x: int, y: int) -> Tree:
        return self._trees[y][x]

    def get_row(
        self,
        y: int,
        direction: Direction,
        start_x: int | None = None,
    ) -> Iterable[Tree]:
        column = self._trees[y]
        size = len(column)

        start_index: int
        if start_x is None:
            if direction == Direction.ascending:
                start_index = 0
            else:
                start_index = size - 1
        else:
            start_index = start_x

        stop_index = size if direction == Direction.ascending else -1
        for index in range(start_index, stop_index, direction):
            yield column[index]

    def get_column(
        self,
        x: int,
        direction: Direction,
        start_y: int | None = None,
    ) -> Iterable[Tree]:
        trees = self._trees
        size = len(trees)

        start_index: int
        if start_y is None:
            if direction == Direction.ascending:
                start_index = 0
            else:
                start_index = size - 1
        else:
            start_index = start_y

        stop_index = size if direction == Direction.ascending else -1
        for index in range(start_index, stop_index, direction):
            yield trees[index][x]

    @classmethod
    def parse(cls, lines: Iterable[str]) -> Grid:
        trees: list[list[Tree]] = []
        for y, line in enumerate(lines):
            row: list[Tree] = []
            for x, char in enumerate(line):
                height = int(char)
                row.append(
                    Tree(
                        position=Position(x, y),
                        height=height,
                    )
                )
            trees.append(row)

        return cls(trees)

    def __repr__(self) -> str:
        result = ""
        for row in (self.get_row(y, Direction.ascending) for y in range(self.height)):
            result += "".join(str(tree.height) for tree in row)
            result += "\n"
        return result


class Task1(Task):
    def find_visible(self, grid: Grid) -> set[tuple[int, int]]:
        visible: set[tuple[int, int]] = set()

        for y in range(grid.height):
            for direction in Direction:
                current_max = -1
                for tree in grid.get_row(y, direction):
                    if tree.height > current_max:
                        visible.add(tree.position)
                        current_max = tree.height

        for x in range(grid.width):
            for direction in Direction:
                current_max = -1
                for tree in grid.get_column(x, direction):
                    if tree.height > current_max:
                        visible.add(tree.position)
                        current_max = tree.height

        return visible

    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> str | int:
        grid = Grid.parse(input_lines)
        visible = self.find_visible(grid)
        return len(visible)


class Task2(Task):
    def calculate_scenic_score(self, grid: Grid, x: int, y: int) -> int:
        distances = [0, 0, 0, 0]
        index = 0
        candidate = grid.get_tree(x, y)
        for get_line, start_index, line_index in [
            (grid.get_row, x, y),
            (grid.get_column, y, x),
        ]:
            for direction in Direction:
                for tree in get_line(line_index, direction, start_index):
                    if tree == candidate:
                        continue

                    distances[index] = len(candidate.position - tree.position)
                    if tree.height >= candidate.height:
                        break

                index += 1

        return reduce(operator.mul, distances, 1)

    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> str | int:
        grid = Grid.parse(input_lines)
        return max(
            self.calculate_scenic_score(grid, x, y)
            for x in range(grid.width)
            for y in range(grid.height)
        )


day = Day([Task1(), Task2()])
