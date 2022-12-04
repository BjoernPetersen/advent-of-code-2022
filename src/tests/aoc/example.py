from pathlib import Path


class ExampleData:
    def __init__(self, day: int, task: int):
        self._dir = Path("inputs", "day{:02}".format(day), "task{}".format(task))

    def provide_path(self, index: int = 0) -> Path:
        return self._dir / f"example{index}.txt"
