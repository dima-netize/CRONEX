import pytest

from novacore.models.novacore import NovaCoreMini
from novacore.models.nova_block import HybridNovaBlock


def test_conditional_shift_flow():
    model = NovaCoreMini()
    out = model.run("STORE_COLOR C4 | SHIFT N2 | SHIFT N3 | QUERY")
    assert out.answer == "C9"
    assert out.verified is True
    assert 0.0 <= out.block_signal <= 1.0


def test_binding_flow():
    model = NovaCoreMini()
    out = model.run("PAIR S3 C7 | QUERY S3")
    assert out.answer == "C7"
    assert out.verified is True


def test_reverse_binding_flow():
    model = NovaCoreMini()
    out = model.run("PAIR S3 C7 | QUERY C7")
    assert out.answer == "S3"
    assert out.verified is True


def test_stateless_between_runs():
    model = NovaCoreMini()
    first = model.run("STORE_COLOR C1 | SHIFT N1 | QUERY")
    second = model.run("STORE_COLOR C1 | QUERY")
    assert first.answer == "C2"
    assert second.answer == "C1"


def test_missing_binding_returns_unverified():
    model = NovaCoreMini(max_retries=0)
    out = model.run("QUERY S42")
    assert out.verified is False
    assert "Немає пари" in out.verifier_reason


def test_hybrid_block_weights_must_sum_to_one():
    with pytest.raises(ValueError):
        HybridNovaBlock(0.5, 0.5, 0.5)
