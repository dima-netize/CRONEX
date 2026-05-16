from __future__ import annotations

from dataclasses import dataclass

from .causal_model import CausalWorldModel
from .memory import MemoryCell, WorkingMemory
from .object_parser import Operation
from .tooling import ToolRegistry


@dataclass
class EngineResult:
    message: str


class OperationEngine:
    @staticmethod
    def _parse_color(token: str) -> int:
        if not token.startswith("C"):
            raise ValueError(f"Невірний токен кольору: {token}")
        return int(token[1:])

    @staticmethod
    def _to_color(value: int) -> str:
        return f"C{value}"

    @staticmethod
    def _parse_shift(token: str) -> int:
        if not token.startswith("N"):
            raise ValueError(f"Невірний токен зсуву: {token}")
        return int(token[1:])

    def run(self, op: Operation, memory: WorkingMemory, causal_model: CausalWorldModel, allow_tools: bool = True) -> EngineResult:
        if op.name == "STORE_COLOR":
            color = op.args[0]
            self._parse_color(color)
            memory.write(MemoryCell(key="base_color", type="color", value=color))
            if not memory.exists("total_shift"):
                memory.write(MemoryCell(key="total_shift", type="int", value=0))
            causal_model.record("STORE_COLOR", f"base_color={color}")
            return EngineResult(f"stored {color}")

        if op.name == "SHIFT":
            shift = self._parse_shift(op.args[0])
            if not memory.exists("total_shift"):
                memory.write(MemoryCell(key="total_shift", type="int", value=0))
            current = memory.read("total_shift").value
            memory.update("total_shift", current + shift)
            causal_model.record("SHIFT", f"total_shift={current + shift}")
            return EngineResult(f"shifted +{shift}")

        if op.name == "IF_SHIFT_GT":
            threshold = int(op.args[0])
            action = op.args[1].upper()
            value = memory.read("total_shift").value if memory.exists("total_shift") else 0
            if value > threshold and action == "STORE_COLOR":
                color = op.args[2]
                memory.write(MemoryCell(key="base_color", type="color", value=color))
                causal_model.record("IF_SHIFT_GT", f"base_color={color}")
                return EngineResult(f"if_applied STORE_COLOR {color}")
            return EngineResult("if_skipped")

        if op.name == "TOOL_ADD":
            if not allow_tools:
                raise PermissionError("TOOL_ADD disabled in current governance mode")
            a = int(op.args[0])
            b = int(op.args[1])
            out_key = op.args[2]
            val = ToolRegistry.add(a, b)
            memory.write(MemoryCell(key=out_key, type="int", value=val))
            causal_model.record("TOOL_ADD", f"{out_key}={val}")
            return EngineResult(f"tool_add {out_key}={val}")

        if op.name == "PAIR":
            left, right = op.args
            memory.write(MemoryCell(key=f"bind:{left}", type="binding", value=right))
            memory.write(MemoryCell(key=f"bind_rev:{right}", type="binding", value=left))
            causal_model.record("PAIR", f"bind:{left}<->{right}")
            return EngineResult(f"paired {left}<->{right}")

        if op.name == "QUERY":
            if op.args:
                key = op.args[0]
                if memory.exists(f"bind:{key}"):
                    value = memory.read(f"bind:{key}").value
                    causal_model.record("QUERY", f"bind:{key}->{value}")
                    return EngineResult(value)
                if memory.exists(f"bind_rev:{key}"):
                    value = memory.read(f"bind_rev:{key}").value
                    causal_model.record("QUERY", f"bind_rev:{key}->{value}")
                    return EngineResult(value)
                if memory.exists(key):
                    value = memory.read(key).value
                    causal_model.record("QUERY", f"mem:{key}->{value}")
                    return EngineResult(str(value))
                raise KeyError(f"Немає пари для {key}")

            base = self._parse_color(memory.read("base_color").value)
            shift = memory.read("total_shift").value
            answer = self._to_color(base + shift)
            causal_model.record("QUERY", f"color={answer}")
            return EngineResult(answer)

        raise ValueError(f"Невідома операція: {op.name}")
