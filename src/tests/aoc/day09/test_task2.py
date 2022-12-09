import pytest

from aoc.day09 import day
from aoc.spi import Task
from tests.aoc.example import ExampleData


@pytest.fixture
def task() -> Task:
    return day.get_task_or_raise(2)


@pytest.fixture()
def test_data() -> ExampleData:
    return ExampleData(9, 2)


@pytest.mark.parametrize(
    "index, expected",
    [
        (0, 1),
        (1, 36),
    ],
)
def test_examples(task, test_data, tmp_path, index, expected):
    path = test_data.provide_path(index)
    result = task.run(path, tmp_path)
    assert result == expected
