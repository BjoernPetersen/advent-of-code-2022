from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Callable, TypeAlias

from more_itertools import chunked

from aoc.spi import Day, Task


@dataclass
class Test:
    divisor: int
    outcomes: tuple[int, int]

    @classmethod
    def parse(cls, decl: list[str]) -> Test:
        return cls(
            divisor=int(decl[0].rsplit(" ", maxsplit=1)[1]),
            outcomes=(int(decl[1][-1]), int(decl[2][-1])),
        )

    def __call__(self, number: int) -> int:
        return self.outcomes[0] if number % self.divisor == 0 else self.outcomes[1]


Operation: TypeAlias = Callable[[int], int]


def parse_operation(decl: str) -> Operation:
    relevant = decl[len("new = old ") :]
    operator, operand = relevant.split()
    literal = 0 if operand == "old" else int(operand)

    def multiply_old(old: int) -> int:
        return old**2

    def multiply_literal(old: int) -> int:
        return old * literal

    def add_old(old: int) -> int:
        return 2 * old

    def add_literal(old: int) -> int:
        return old + literal

    if operator == "*":
        if literal == 0:
            return multiply_old
        return multiply_literal

    if operator == "+":
        if literal == 0:
            return add_old
        return add_literal

    raise ValueError(f"Unknown operator: {operator}")


@dataclass
class Monkey:
    id: int
    items: list[int]
    operation: Operation
    test: Test
    inspected_items: int = 0

    @classmethod
    def parse(cls, decl: list[str]) -> Monkey:
        return cls(
            id=int(decl[0][7]),
            items=[int(item.strip()) for item in decl[1].split(":")[1].split(",")],
            operation=parse_operation(decl[2].split(":")[1].lstrip()),
            test=Test.parse(decl[3:6]),
        )

    def inspect(self):
        self.items = [self.operation(item) for item in self.items]
        self.inspected_items += len(self.items)

    def lose_interest(self):
        self.items = [item // 3 for item in self.items]

    def throw_items(self, throw: Callable[[int, int], None]):
        items = self.items
        self.items = []
        for item in items:
            target = self.test(item)
            throw(item, target)

    def catch(self, item: int):
        self.items.append(item)


def parse_input(input_lines: Iterable[str]) -> list[Monkey]:
    return [Monkey.parse(declaration) for declaration in chunked(input_lines, 7)]


class Task1(Task):
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> str | int:
        monkeys = parse_input(input_lines)
        for _ in range(20):
            for monkey in monkeys:
                monkey.inspect()
                monkey.lose_interest()
                monkey.throw_items(lambda item, target: monkeys[target].catch(item))

        monkeys.sort(key=lambda m: m.inspected_items, reverse=True)
        return monkeys[0].inspected_items * monkeys[1].inspected_items


class Task2(Task):
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> str | int:
        monkeys = parse_input(input_lines)

        def catch(item: int, target: int):
            monkeys[target].catch(item)

        for _ in range(10_000):
            for monkey in monkeys:
                monkey.inspect()
                monkey.throw_items(catch)

        monkeys.sort(key=lambda m: m.inspected_items, reverse=True)
        return monkeys[0].inspected_items * monkeys[1].inspected_items


day = Day([Task1(), Task2()])
