import pytest

from aoc.day08 import day
from aoc.spi import Task
from tests.aoc.example import ExampleData


@pytest.fixture
def task() -> Task:
    return day.get_task_or_raise(2)


@pytest.fixture()
def test_data() -> ExampleData:
    return ExampleData(8, 2)


def test_example(task, test_data, tmp_path):
    path = test_data.provide_path()
    result = task.run(path, tmp_path)
    assert result == 0
