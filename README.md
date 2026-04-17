# Processor Design Semester Project - Task 4

## How to run
### Run with the default example values
Default values are:
- `A = 1`
- `B = 1`
- `C = 0`
- `D = 1`

### Command:
python3 main.py --write-output-file

## Project structure
task4/
- ├── “README.md”
- ├── “main.py”: for running the simulation
- ├── “alu.py”: for AND / OR execution and inversion
- ├── “control_unit.py”: for decoding and control signals
- ├── “instruction.py”
- ├── “instruction_memory.py”: for the fixed program
- ├── “mux.py”: for selecting normal or inverted ALU input
- ├── “processor.py”: for integrating the full single-cycle datapath
- ├── “register_file.py”: for the register file
- └── “sample_run_output.txt”


## Register mapping used in the program
The assignment states:
- `t0 = A`
- `t1 = B`
- `t2 = C`
- `t3 = D`
Intermediate / output registers:
- `t4 = A & B`
- `t6 = (~C) & D`
- `t0 = final result`

## Program executed by the processor
- and  t4, t0, t1     # t4 = A & B
- and  t6, t2, t3     # t6 = (~C) & D
- or   t0, t4, t6     # t0 = t4 | t6

## Datapath explanation
The processor follows a single-cycle execution model.
Each instruction completes in one cycle with these steps:
1. Fetch
2. Decode
3. Execute
4. Write-back

The control unit decodes the instruction and generates three main control signals:
- ALU operation
- inversion flag
- register write enable