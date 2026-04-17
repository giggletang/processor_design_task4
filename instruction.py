from dataclasses import dataclass


@dataclass(frozen=True)
class Instruction:
    """Simple R-type instruction for the task-4 single-cycle processor."""

    opcode: int
    rs: str
    rt: str
    rd: str
    funct: int
    asm: str

    FUNCT_AND = 0x24
    FUNCT_OR = 0x25
    # Custom function code: same opcode family, but with ALU input inversion enabled.
    FUNCT_ANDN = 0x2C

    @classmethod
    def and_(cls, rd: str, rs: str, rt: str) -> "Instruction":
        return cls(
            opcode=0x00,
            rs=rs,
            rt=rt,
            rd=rd,
            funct=cls.FUNCT_AND,
            asm=f"and {rd}, {rs}, {rt}",
        )

    @classmethod
    def andn(cls, rd: str, rs: str, rt: str) -> "Instruction":
        return cls(
            opcode=0x00,
            rs=rs,
            rt=rt,
            rd=rd,
            funct=cls.FUNCT_ANDN,
            asm=f"and {rd}, {rs}, {rt}   # invert first ALU input before AND",
        )

    @classmethod
    def or_(cls, rd: str, rs: str, rt: str) -> "Instruction":
        return cls(
            opcode=0x00,
            rs=rs,
            rt=rt,
            rd=rd,
            funct=cls.FUNCT_OR,
            asm=f"or  {rd}, {rs}, {rt}",
        )
