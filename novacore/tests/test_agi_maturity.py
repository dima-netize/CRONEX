from novacore.models.agi_maturity import classify_maturity


def test_maturity_classification_order():
    assert classify_maturity(0.2).level == "L1-Prototype"
    assert classify_maturity(0.6).level == "L3-Agentic"
    assert classify_maturity(0.86).level == "L4-Pre-AGI"
