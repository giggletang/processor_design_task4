# 2-to-1 multiplexer used to choose normal or inverted ALU input

class Mux:
    """Simple 2-to-1 multiplexer."""

    @staticmethod
    def select(input0: int, input1: int, select_signal: bool) -> int:
        return input1 if select_signal else input0
