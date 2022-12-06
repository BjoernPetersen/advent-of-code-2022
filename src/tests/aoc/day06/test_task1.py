import pytest

from aoc.day06 import day
from aoc.spi import Task


@pytest.fixture
def task() -> Task:
    return day.get_task_or_raise(1)


@pytest.mark.parametrize(
    ["message", "expected"],
    [
        ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7),
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
        ("nppdvjthqldpwncqszvftbrmjlhg", 6),
        ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11),
    ],
)
def test_examples(task, message: str, expected: int, tmp_path):
    result = task.calculate([message], tmp_path)
    assert result == expected
