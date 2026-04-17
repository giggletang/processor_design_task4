# 32-bit ALU supporting AND, OR, and input inversion on operand A

class ALU:
    """32-bit ALU that supports AND / OR and optional inversion of input A."""

    MASK_32 = 0xFFFFFFFF

    def execute(self, a: int, b: int, alu_op: str, invert_a: bool = False) -> dict:
        original_a = a & self.MASK_32
        b = b & self.MASK_32
        effective_a = (~original_a) & self.MASK_32 if invert_a else original_a

        if alu_op == "AND":
            result = effective_a & b
        elif alu_op == "OR":
            result = effective_a | b
        else:
            raise ValueError(f"Unsupported ALU operation: {alu_op}")

        return {
            "original_a": original_a,
            "effective_a": effective_a,
            "b": b,
            "result": result & self.MASK_32,
        }
