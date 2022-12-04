import abc
from dataclasses import dataclass
from pathlib import Path


class Task(abc.ABC):
    @abc.abstractmethod
    def run(self, input_file: Path, working_dir: Path) -> str | int:
        pass


@dataclass(frozen=True)
class Day:
    tasks: list[Task]

    def get_task_or_raise(self, task: int) -> Task:
        if task > len(self.tasks):
            raise NotImplementedError(f"Task {task} is not implemented yet.")

        if task < 1:
            raise ValueError("Task number must be greater than 1")

        return self.tasks[task - 1]
