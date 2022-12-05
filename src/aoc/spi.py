import abc
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


class Task(abc.ABC):
    @abc.abstractmethod
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> str | int:
        pass

    def run(self, file: Path, working_dir: Path) -> str | int:
        with open(file) as f:
            return self.calculate(
                (line.rstrip("\n") for line in f.readlines()),
                working_dir,
            )


@dataclass(frozen=True)
class Day:
    tasks: list[Task]

    def get_task_or_raise(self, task: int) -> Task:
        if task > len(self.tasks):
            raise NotImplementedError(f"Task {task} is not implemented yet.")

        if task < 1:
            raise ValueError("Task number must be greater than 1")

        return self.tasks[task - 1]
