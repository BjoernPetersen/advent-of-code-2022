from __future__ import annotations

import abc
import pathlib
from typing import Iterable

from aoc.spi import Day
from aoc.spi import Task


class Path(abc.ABC):
    def __init__(self, name: str, parent: Directory | None):
        self.name = name
        self.parent = parent

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Path):
            return False

        return o.name == self.name and o.parent == self.parent

    def __hash__(self) -> int:
        return hash((self.name, self.parent))

    @abc.abstractmethod
    def files(self) -> Iterable[File]:
        pass

    @property
    @abc.abstractmethod
    def size(self) -> int:
        pass


class Directory(Path):
    def __init__(self, name: str, parent: Directory | None):
        super().__init__(name, parent)
        self._children: set[Path] = set()

    def add_file(self, name: str, size: int) -> File:
        file = File(name, size, self)
        self._children.add(file)
        return file

    def add_directory(self, name: str) -> Directory:
        directory = Directory(name, self)
        if directory in self._children:
            for child in self._children:
                if child.name == name:
                    if isinstance(child, Directory):
                        return child
                    else:
                        raise ValueError(
                            f"Tried to add directory {name} even though"
                            f" file with the same name exists"
                        )
            raise NotImplementedError("Unreachable code reached")
        else:
            self._children.add(directory)
            return directory

    def list(self) -> Iterable[Path]:
        yield from self._children

    def files(self) -> Iterable[File]:
        for child in self._children:
            yield from child.files()

    def directories(self) -> Iterable[Directory]:
        yield self
        for child in self._children:
            if isinstance(child, Directory):
                yield from child.directories()

    @property
    def size(self) -> int:
        return sum(file.size for file in self.files())


class File(Path):
    def __init__(self, name: str, size: int, parent: Directory):
        super().__init__(name, parent)
        self._size = size

    @property
    def size(self) -> int:
        return self._size

    def files(self) -> Iterable[File]:
        yield self


class Command(abc.ABC):
    def __init__(self, prompt: str, output: list[str]):
        self.prompt = prompt
        self.output = output

    @property
    def args(self) -> list[str]:
        return self.prompt.split()[1:]

    @abc.abstractmethod
    def synthesize(self, working_dir: Directory) -> Directory:
        pass


class List(Command):
    def synthesize(self, working_dir: Directory) -> Directory:
        content = self.output
        for item in content:
            size, filename = item.split(maxsplit=1)
            if size == "dir":
                continue

            working_dir.add_file(name=filename, size=int(size))

        return working_dir


class ChangeDirectory(Command):
    def synthesize(self, working_dir: Directory) -> Directory:
        target = self.args[0]
        if target == "..":
            parent = working_dir.parent

            if not parent:
                raise ValueError("Can't cd .. from root!")

            return parent

        return working_dir.add_directory(target)

    def __repr__(self):
        return " ".join([self.prompt, *self.output])


def parse_command(lines: list[str]) -> Command:
    prompt = lines[0][2:]
    command_name = prompt.split()[0]
    if command_name == "ls":
        return List(prompt, lines[1:])
    elif command_name == "cd":
        return ChangeDirectory(prompt, lines[1:])
    else:
        raise ValueError(f"Unknown command: {command_name}")


def generate_directory(commands: list[Command]) -> Directory:
    if commands[0].prompt != "cd /":
        raise ValueError("Input doesn't start with cd /")

    root_dir = Directory("/", parent=None)
    working_dir = root_dir
    for command in commands[1:]:
        working_dir = command.synthesize(working_dir)
    return root_dir


def parse_input(input_lines: Iterable[str]) -> Directory:
    commands: list[Command] = []
    batch: list[str] = []
    for line in input_lines:
        if line.startswith("$"):
            # new command
            if batch:
                commands.append(parse_command(batch))
            batch = [line]
        else:
            batch.append(line)
    commands.append(parse_command(batch))

    return generate_directory(commands)


class Task1(Task):
    def calculate(
        self, input_lines: Iterable[str], working_dir: pathlib.Path
    ) -> str | int:
        root = parse_input(input_lines)
        total_size = 0
        for directory in root.directories():
            size = directory.size
            if size <= 100000:
                total_size += size

        return total_size


class Task2(Task):
    def calculate(
        self, input_lines: Iterable[str], working_dir: pathlib.Path
    ) -> str | int:
        root = parse_input(input_lines)
        available = 70000000
        required = 30000000
        free = available - root.size
        needed = required - free

        return min(
            directory.size
            for directory in root.directories()
            if directory.size >= needed
        )


day = Day([Task1(), Task2()])
