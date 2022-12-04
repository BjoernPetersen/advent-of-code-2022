import importlib
import os
import sys
from pathlib import Path

import click

from aoc.spi import Day


def _prepare_environment(
    day: int,
    task: int,
    input_file_override: Path | None,
) -> tuple[Path, Path]:
    day_dir = Path("day{:02}".format(day))

    input_file = input_file_override or Path("inputs") / day_dir / Path("input.txt")
    working_dir = Path("outputs") / day_dir / Path(f"task{task}")

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


@click.group()
def main():
    pass


@main.group()
@click.pass_context
@click.argument("day", type=int)
def day(ctx, day: int):
    ctx.obj = day


@day.command()
@click.pass_obj
@click.argument("task", type=int)
@click.option(
    "input_file", "--input", "-i", type=click.Path(exists=True, dir_okay=False)
)
def task(day: int, task: int, input_file: Path | None):
    try:
        paths = _prepare_environment(
            day=day,
            task=task,
            input_file_override=input_file,
        )
    except OSError as e:
        print(e)
        sys.exit(1)

    try:
        day_impl: Day = _load_day(day)
        task_impl = day_impl.get_task_or_raise(task)
    except NotImplementedError as e:
        print(e)
        sys.exit(2)

    result = task_impl.run(*paths)
    print(f"Result for day {day} task {task} is {result}")
