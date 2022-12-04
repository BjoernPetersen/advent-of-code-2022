import importlib
import os
import sys
from pathlib import Path

import click

from aoc.spi import Day


def _prepare_environment(day: int, task: int) -> tuple[Path, Path]:
    task_dir = Path("day{:02}".format(day), "task{}".format(task))
    input_file = Path("inputs") / task_dir / Path("input.txt")
    working_dir = Path("outputs") / task_dir

    if not input_file.is_file():
        raise OSError(f"Input file '{input_file}' does not exist")

    if working_dir.exists():
        if not working_dir.is_dir():
            raise OSError(f"'{working_dir}' exists and is not a directory!")

        os.rmdir(working_dir)

    working_dir.mkdir(parents=True)

    return input_file, working_dir


def _load_day(day: int) -> Day:
    try:
        day_module = importlib.import_module("aoc.day{:02}".format(day))
    except ModuleNotFoundError:
        raise NotImplementedError(f"Day {day} is not implemented yet")
    return day_module.day


@click.command()
@click.argument("day", type=int)
@click.argument("task", type=int)
def main(day: int, task: int):
    try:
        paths = _prepare_environment(day=day, task=task)
    except OSError as e:
        print(e)
        sys.exit(1)

    try:
        day_impl: Day = _load_day(day)
        task_impl = day_impl.get_task_or_raise(task)
    except NotImplementedError as e:
        print(e)
        sys.exit(2)

    task_impl.run(*paths)
