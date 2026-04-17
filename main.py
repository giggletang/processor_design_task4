# CSC 6210 - Processor Design Task 4
# Zihan Tang

import argparse
from pathlib import Path
from typing import Dict, List

from alu import ALU
from control_unit import ControlUnit
from instruction import Instruction
from instruction_memory import InstructionMemory
from processor import SingleCycleProcessor
from register_file import RegisterFile

REGISTER_ORDER = [f"t{i}" for i in range(7)]
OUTPUT_PATH = Path("sample_run_output.txt")


def build_program() -> InstructionMemory:
    program = [
        Instruction.and_("t4", "t0", "t1"),
        Instruction.andn("t6", "t2", "t3"),
        Instruction.or_("t0", "t4", "t6"),
    ]
    return InstructionMemory(program)


def create_processor(a: int, b: int, c: int, d: int) -> SingleCycleProcessor:
    register_file = RegisterFile({"t0": a, "t1": b, "t2": c, "t3": d})
    return SingleCycleProcessor(
        instruction_memory=build_program(),
        register_file=register_file,
        control_unit=ControlUnit(),
        alu=ALU(),
    )


def format_trace(trace: List[Dict], a: int, b: int, c: int, d: int) -> str:
    lines: List[str] = []
    lines.append("Task 4 - Single-Cycle Processor Execution Trace")
    lines.append("=" * 60)
    lines.append(f"Input values: A={a}, B={b}, C={c}, D={d}")
    lines.append("Target equation: Y = A·B + C'·D")
    lines.append("")

    for step_no, item in enumerate(trace, start=1):
        lines.append(f"Instruction {step_no}: {item['instruction']}")
        lines.append(f"  PC: {item['pc']}")
        lines.append(f"  Decoded fields: {item['decoded_fields']}")
        lines.append(f"  Register reads: {item['read_values']}")
        lines.append(f"  MUX activity: {item['mux']}")
        lines.append(f"  Control signals: {item['control_signals']}")
        lines.append(
            "  ALU: "
            f"original_a={item['alu']['original_a']}, "
            f"effective_a={item['alu']['effective_a']}, "
            f"b={item['alu']['b']}, "
            f"result={item['alu']['result']}"
        )
        lines.append(f"  Write-back: {item['write_back']}")
        reg_pairs = ", ".join(f"{k}={v}" for k, v in item["registers_after"].items())
        lines.append(f"  Registers after instruction: {reg_pairs}")
        lines.append("")

    final_registers = trace[-1]["registers_after"]
    expected = ((a & b) | (((~c) & 0xFFFFFFFF) & d)) & 0xFFFFFFFF

    lines.append("Intermediate results required by the assignment:")
    lines.append(f"  t4 = A & B = {final_registers['t4']}")
    lines.append(f"  t6 = (~C) & D = {final_registers['t6']}")
    lines.append(f"  t0 = final result Y = {final_registers['t0']}")
    lines.append("")
    lines.append(f"Expected logical result = {expected}")
    lines.append(f"Validation PASSED = {final_registers['t0'] == expected}")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Task 4 single-cycle processor simulation.")
    parser.add_argument("--A", type=int, default=1, help="Initial value of A (loaded into t0)")
    parser.add_argument("--B", type=int, default=1, help="Initial value of B (loaded into t1)")
    parser.add_argument("--C", type=int, default=0, help="Initial value of C (loaded into t2)")
    parser.add_argument("--D", type=int, default=1, help="Initial value of D (loaded into t3)")
    parser.add_argument(
        "--write-output-file",
        action="store_true",
        help="Write the full execution trace to sample_run_output.txt",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    processor = create_processor(args.A, args.B, args.C, args.D)
    trace = processor.run(register_order=REGISTER_ORDER)
    report = format_trace(trace, args.A, args.B, args.C, args.D)
    print(report)

    if args.write_output_file:
        OUTPUT_PATH.write_text(report, encoding="utf-8")
        print(f"\nSaved output to {OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()
