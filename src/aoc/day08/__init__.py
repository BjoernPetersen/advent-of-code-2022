from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from itertools import pairwise
from pathlib import Path
from typing import Iterable

from aoc.spi import Day
from aoc.spi import Task


class Direction(IntEnum):
    ascending = 1
    descending = -1


@dataclass
class Tree:
    position: tuple[int, int]
    height: int


class Grid:
    def __init__(self, trees: list[list[Tree]]):
        self._trees = trees
        self.height = len(trees)
        self.width = len(trees[0])

    def get_tree(self, x: int, y: int) -> Tree:
        return self._trees[y][x]

    def get_row(self, y: int, direction: Direction) -> Iterable[Tree]:
        column = self._trees[y]
        size = len(column)
        start_index = 0 if direction == Direction.ascending else size - 1
        stop_index = size if direction == Direction.ascending else -1
        for index in range(start_index, stop_index, direction):
            yield column[index]

    def get_column(self, x: int, direction: Direction) -> Iterable[Tree]:
        trees = self._trees
        size = len(trees)
        start_index = 0 if direction == Direction.ascending else size - 1
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
                        position=(x, y),
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
                for pair in pairwise(grid.get_row(y, direction)):
                    if pair[1].height > pair[0].height:
                        visible.add(pair[1].position)
                    else:
                        break

        for x in range(grid.width):
            for direction in Direction:
                for pair in pairwise(grid.get_column(x, direction)):
                    if pair[1].height > pair[0].height:
                        visible.add(pair[1].position)
                    else:
                        break

        for x in range(grid.width):
            visible.add((x, 0))
            visible.add((x, grid.height - 1))

        for y in range(grid.height):
            visible.add((0, y))
            visible.add((grid.width - 1, y))

        return visible

    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> str | int:
        grid = Grid.parse(input_lines)
        visible = self.find_visible(grid)
        return len(visible)


day = Day([Task1()])
