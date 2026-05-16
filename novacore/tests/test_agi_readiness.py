from novacore.models.agi_readiness import estimate_agi_readiness


def test_agi_readiness_overall_range():
    score = estimate_agi_readiness(True, True, True, True, True)
    assert 0.0 <= score.overall <= 1.0


def test_agi_readiness_drops_without_capabilities():
    strong = estimate_agi_readiness(True, True, True, True, True)
    weak = estimate_agi_readiness(False, False, False, False, False)
    assert strong.overall > weak.overall
