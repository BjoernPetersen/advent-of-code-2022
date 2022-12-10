import abc
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Callable

from aoc.spi import Day, Task


class Clock(abc.ABC):
    @abc.abstractmethod
    def tick(self, n: int = 1):
        pass


class FastClock(Clock):
    def tick(self, n: int = 1):
        pass


class ObservableClock(Clock):
    def __init__(self, on_tick: Callable[[int], None]):
        self._cycles: int = 1
        self._on_tick = on_tick

    def tick(self, n: int = 1):
        cycles = self._cycles
        for i in range(n):
            self._on_tick(cycles + i)
        self._cycles = cycles + n


@dataclass
class Registers:
    x: int = 1


class Instruction(abc.ABC):
    @abc.abstractmethod
    def execute(self, clock: Clock, registers: Registers):
        pass


class Noop(Instruction):
    def execute(self, clock: Clock, registers: Registers):
        clock.tick()


class AddX(Instruction):
    def __init__(self, operand: int):
        self._operand = operand

    def execute(self, clock: Clock, registers: Registers):
        clock.tick(2)
        registers.x += self._operand


class Cpu:
    def __init__(self):
        self._registers = Registers()

    @property
    def registers(self) -> Registers:
        return self._registers

    def run(self, clock: Clock, program: Iterable[Instruction]):
        registers = self._registers

        for instruction in program:
            instruction.execute(clock, registers)


def compile_program(lines: Iterable[str]) -> Iterable[Instruction]:
    for line in lines:
        parts = line.split(" ")
        operation = parts[0]

        if operation == "noop":
            yield Noop()
        elif operation == "addx":
            yield AddX(int(parts[1]))
        else:
            raise ValueError(f"Unknown operation: {operation}")


class Task1(Task):
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> str | int:
        program = compile_program(input_lines)
        result: list[int] = []
        cpu = Cpu()

        def on_tick(count: int):
            if count == 20 or (count - 20) % 40 == 0:
                result.append(count * cpu.registers.x)

        cpu.run(ObservableClock(on_tick), program)
        return sum(result)


class Crt:
    def __init__(self) -> None:
        self._width = 40
        self._height = 6
        self._pixels: list[str] = ["."] * self._width * self._height

    def draw(self, cycle: int, registers: Registers):
        x = (cycle - 1) % self._width
        if abs(x - registers.x) <= 1:
            self._pixels[cycle - 1] = "#"

    def render(self) -> str:
        width = self._width
        height = self._height
        pixels = self._pixels
        return "\n".join(
            "".join(pixels[row * width : (row + 1) * width]) for row in range(height)
        )


class Task2(Task):
    def calculate(self, input_lines: Iterable[str], working_dir: Path) -> str | int:
        program = compile_program(input_lines)
        cpu = Cpu()
        crt = Crt()

        def on_tick(count: int):
            crt.draw(count, cpu.registers)

        cpu.run(ObservableClock(on_tick), program)
        rendered = crt.render()
        return rendered


day = Day([Task1(), Task2()])
