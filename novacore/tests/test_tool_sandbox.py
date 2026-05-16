import pytest
from novacore.models.operation_engine import OperationEngine
from novacore.models.object_parser import Operation
from novacore.models.memory import WorkingMemory
from novacore.models.causal_model import CausalWorldModel


def test_tool_add_blocked_in_cautious_policy():
    eng = OperationEngine()
    with pytest.raises(PermissionError):
        eng.run(Operation(name="TOOL_ADD", args=["1", "2", "SUM"]), WorkingMemory(), CausalWorldModel(), allow_tools=False)
