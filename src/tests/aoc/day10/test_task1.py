import pytest

from aoc.day10 import day
from aoc.spi import Task
from tests.aoc.example import ExampleData


@pytest.fixture
def task() -> Task:
    return day.get_task_or_raise(1)


@pytest.fixture()
def test_data() -> ExampleData:
    return ExampleData(10, 1)


def test_example(task, test_data, tmp_path):
    path = test_data.provide_path(1)
    result = task.run(path, tmp_path)
    assert result == 13140
