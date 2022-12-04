import pytest

from aoc.day01 import Task1
from aoc.spi import Task
from tests.aoc.example import ExampleData


@pytest.fixture
def task() -> Task:
    return Task1()


@pytest.fixture()
def test_data() -> ExampleData:
    return ExampleData(1, 1)


def test_example(task, test_data, tmp_path):
    path = test_data.provide_path()
    result = task.run(path, tmp_path)
    assert result == "24000"
