from novacore.training.l5_gate_dashboard import public_sota_eval


def test_public_sota_eval_nonzero():
    v = public_sota_eval()
    assert v > 0
