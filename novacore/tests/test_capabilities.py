from novacore.models.novacore import NovaCoreMini


def test_describe_capabilities_has_core_items():
    model = NovaCoreMini()
    lines = model.describe_capabilities()
    assert any("Object Parsing" in line for line in lines)
    assert any("Verification" in line for line in lines)
