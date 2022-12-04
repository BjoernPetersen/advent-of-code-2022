import pytest

from aoc.day02 import Task2
from aoc.spi import Task
from tests.aoc.example import ExampleData


@pytest.fixture
def task() -> Task:
    return Task2()


@pytest.fixture()
def test_data() -> ExampleData:
    return ExampleData(2, 2)


def test_example(task, test_data, tmp_path):
    path = test_data.provide_path()
    result = task.run(path, tmp_path)
    assert result == 12


def test_win_against_scissor(task, test_data, tmp_path):
    result = task.calculate(["C Z"], tmp_path)
    # 1 for rocks, 6 for winning
    assert result == 7


def test_lose_against_rocks(task, test_data, tmp_path):
    result = task.calculate(["A X"], tmp_path)
    # 3 for scissor, 0 for losing
    assert result == 3
