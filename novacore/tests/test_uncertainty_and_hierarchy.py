from novacore.models.novacore import NovaCoreMini
from novacore.models.uncertainty import UncertaintyCalibrator
from novacore.models.hierarchical_planner import HierarchicalPlanner
from novacore.models.object_parser import ObjectParser
from novacore.models.memory import WorkingMemory, MemoryCell


def test_uncertainty_interval_bounds():
    c = UncertaintyCalibrator().calibrate(0.7, retries_used=1, trace_len=4)
    assert 0.0 <= c.lower <= c.mean <= c.upper <= 1.0


def test_hierarchical_planner_has_subgoals():
    ops = ObjectParser().parse("STORE_COLOR C1 | SHIFT N1 | QUERY")
    hp = HierarchicalPlanner().build(ops)
    assert len(hp.subgoals) == 3


def test_memory_prune_removes_low_confidence_cells():
    m = WorkingMemory()
    m.write(MemoryCell(key="a", type="x", value=1, confidence=0.1))
    m.write(MemoryCell(key="b", type="x", value=1, confidence=0.9))
    removed = m.prune(min_confidence=0.2)
    assert removed == 1
    assert not m.exists("a") and m.exists("b")


def test_output_has_confidence_interval():
    out = NovaCoreMini(max_retries=0).run("STORE_COLOR C1 | QUERY")
    assert out.confidence_lower <= out.confidence_upper
