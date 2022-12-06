import pytest

from aoc.day06 import day
from aoc.spi import Task


@pytest.fixture
def task() -> Task:
    return day.get_task_or_raise(2)


@pytest.mark.parametrize(
    ["message", "expected"],
    [
        ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
        ("nppdvjthqldpwncqszvftbrmjlhg", 23),
        ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26),
    ],
)
def test_example(task, message: str, expected: int, tmp_path):
    result = task.calculate([message], tmp_path)
    assert result == expected
