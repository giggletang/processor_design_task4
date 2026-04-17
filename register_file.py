#  register file with two read ports and one write port

from typing import Dict, Iterable, Optional, Tuple


class RegisterFile:
    """32-bit register file with named temporary registers t0..t6."""

    MASK_32 = 0xFFFFFFFF

    def __init__(self, registers: Optional[Dict[str, int]] = None):
        self._registers: Dict[str, int] = {f"t{i}": 0 for i in range(7)}
        if registers:
            for name, value in registers.items():
                self.write(name, value)

    def read(self, register: str) -> int:
        self._require_valid_register(register)
        return self._registers[register]

    def read_pair(self, rs: str, rt: str) -> Tuple[int, int]:
        return self.read(rs), self.read(rt)

    def write(self, register: str, value: int) -> None:
        self._require_valid_register(register)
        self._registers[register] = value & self.MASK_32

    def snapshot(self, register_order: Optional[Iterable[str]] = None) -> Dict[str, int]:
        if register_order is None:
            register_order = self._registers.keys()
        return {name: self._registers[name] for name in register_order}

    def _require_valid_register(self, register: str) -> None:
        if register not in self._registers:
            raise KeyError(f"Unknown register: {register}")
