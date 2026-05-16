from novacore.models.safety import SafetyGuard


def test_long_horizon_program_not_blocked_by_length_guard():
    p = " | ".join(["STORE_COLOR C1"] + ["SHIFT N1"] * 300 + ["QUERY"])
    res = SafetyGuard().check(p)
    assert res.allowed is True
