# instruction decoder and control signal generator

from dataclasses import dataclass

from instruction import Instruction


@dataclass(frozen=True)
class ControlSignals:
    alu_op: str
    invert_a: bool
    reg_write: bool


class ControlUnit:
    """Decodes function fields and generates control signals."""

    def decode(self, instruction: Instruction) -> ControlSignals:
        if instruction.opcode != 0x00:
            raise ValueError(f"Unsupported opcode: {instruction.opcode:#x}")

        if instruction.funct == Instruction.FUNCT_AND:
            return ControlSignals(alu_op="AND", invert_a=False, reg_write=True)
        if instruction.funct == Instruction.FUNCT_ANDN:
            return ControlSignals(alu_op="AND", invert_a=True, reg_write=True)
        if instruction.funct == Instruction.FUNCT_OR:
            return ControlSignals(alu_op="OR", invert_a=False, reg_write=True)

        raise ValueError(f"Unsupported function field: {instruction.funct:#x}")
