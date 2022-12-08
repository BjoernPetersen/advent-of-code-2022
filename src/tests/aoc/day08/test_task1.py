import pytest

from aoc.day08 import day, Grid, Direction, Task1, Tree
from aoc.spi import Task
from tests.aoc.example import ExampleData


@pytest.fixture
def task() -> Task:
    return day.get_task_or_raise(1)


@pytest.fixture()
def test_data() -> ExampleData:
    return ExampleData(8, 1)


def test_grid_parsing(test_data):
    grid = Grid.parse(test_data.provide_lines())
    assert grid.get_tree(0, 0).height == 3
    assert grid.get_tree(4, 1).height == 2
    assert grid.get_tree(4, 4).height == 0
    assert grid.get_tree(0, 4).height == 3


@pytest.mark.parametrize(
    ["x", "direction", "expected"],
    [
        (0, Direction.ascending, [3, 2, 6, 3, 3]),
        (0, Direction.descending, [3, 3, 6, 2, 3]),
        (4, Direction.ascending, [3, 2, 2, 9, 0]),
    ],
)
def test_grid_get_column(test_data, x, direction, expected):
    grid = Grid.parse(test_data.provide_lines())
    assert [tree.height for tree in grid.get_column(x, direction)] == expected


@pytest.mark.parametrize(
    ["y", "direction", "expected"],
    [
        (0, Direction.ascending, [3, 0, 3, 7, 3]),
        (0, Direction.descending, [3, 7, 3, 0, 3]),
        (4, Direction.ascending, [3, 5, 3, 9, 0]),
    ],
)
def test_grid_get_row(test_data, y, direction, expected):
    grid = Grid.parse(test_data.provide_lines())
    assert [tree.height for tree in grid.get_row(y, direction)] == expected


def test_grid_repr(test_data):
    grid = Grid.parse(test_data.provide_lines())
    repr_lines = repr(grid).splitlines(keepends=False)
    assert repr_lines == list(test_data.provide_lines())


def test_example_detailed(task: Task1, test_data):
    grid = Grid.parse(test_data.provide_lines())
    visible = task.find_visible(grid)

    visible_trees: list[list[Tree]] = []
    for y in range(grid.height):
        row: list[Tree] = []
        for x in range(grid.width):
            position = (x, y)
            if position in visible:
                row.append(Tree(position, 1))
            else:
                row.append(Tree(position, 0))
        visible_trees.append(row)

    visible_grid = Grid(visible_trees)
    expected = "\n".join(test_data.provide_lines(1))
    assert repr(visible_grid).strip() == expected


def test_example(task, test_data, tmp_path):
    path = test_data.provide_path()
    result = task.run(path, tmp_path)
    assert result == 21
