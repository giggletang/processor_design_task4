# top-level single-cycle integration

from dataclasses import asdict
from typing import Dict, Iterable, List, Optional

from alu import ALU
from control_unit import ControlUnit
from instruction_memory import InstructionMemory
from mux import Mux
from register_file import RegisterFile


class SingleCycleProcessor:
    """Single-cycle processor simulator for Task 4."""

    def __init__(
        self,
        instruction_memory: InstructionMemory,
        register_file: RegisterFile,
        control_unit: ControlUnit,
        alu: ALU,
    ):
        self.pc = 0
        self.imem = instruction_memory
        self.regs = register_file
        self.control = control_unit
        self.alu = alu

    def step(self, register_order: Optional[Iterable[str]] = None) -> Dict:
        instruction = self.imem.fetch(self.pc)
        control_signals = self.control.decode(instruction)

        rs_value, rt_value = self.regs.read_pair(instruction.rs, instruction.rt)
        inverted_rs_value = (~rs_value) & 0xFFFFFFFF
        selected_a = Mux.select(rs_value, inverted_rs_value, control_signals.invert_a)
        alu_result = self.alu.execute(
            a=rs_value,
            b=rt_value,
            alu_op=control_signals.alu_op,
            invert_a=control_signals.invert_a,
        )

        if control_signals.reg_write:
            self.regs.write(instruction.rd, alu_result["result"])

        log = {
            "pc": self.pc,
            "instruction": instruction.asm,
            "decoded_fields": {
                "opcode": instruction.opcode,
                "rs": instruction.rs,
                "rt": instruction.rt,
                "rd": instruction.rd,
                "funct": instruction.funct,
            },
            "read_values": {
                instruction.rs: rs_value,
                instruction.rt: rt_value,
            },
            "mux": {
                "input0_rs": rs_value,
                "input1_inverted_rs": inverted_rs_value,
                "select_invert_a": control_signals.invert_a,
                "selected_output": selected_a,
            },
            "control_signals": asdict(control_signals),
            "alu": alu_result,
            "write_back": {
                "enable": control_signals.reg_write,
                "destination": instruction.rd,
                "value": alu_result["result"],
            },
            "registers_after": self.regs.snapshot(register_order),
        }

        self.pc += 1
        return log

    def run(self, register_order: Optional[Iterable[str]] = None) -> List[Dict]:
        trace = []
        while self.pc < len(self.imem):
            trace.append(self.step(register_order=register_order))
        return trace
