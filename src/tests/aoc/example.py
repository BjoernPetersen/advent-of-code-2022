from pathlib import Path
from typing import Iterable


class ExampleData:
    def __init__(self, day: int, task: int):
        self._dir = Path("inputs", "day{:02}".format(day))

    def provide_path(self, index: int = 0) -> Path:
        return self._dir / f"example{index}.txt"

    def provide_lines(self, index: int = 0) -> Iterable[str]:
        with open(self.provide_path(index)) as f:
            for line in f:
                yield line.rstrip("\n")
