# instruction input/program memory

from typing import List

from instruction import Instruction


class InstructionMemory:
    """Stores the fixed program for the single-cycle processor."""

    def __init__(self, program: List[Instruction]):
        self.program = program

    def fetch(self, pc: int) -> Instruction:
        if pc < 0 or pc >= len(self.program):
            raise IndexError(f"PC {pc} is outside program memory.")
        return self.program[pc]

    def __len__(self) -> int:
        return len(self.program)
