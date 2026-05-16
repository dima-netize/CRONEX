from novacore.models.toolchain_safety import ToolchainSafetyVerifier


def test_toolchain_safety_ok():
    rep = ToolchainSafetyVerifier().verify(["sandbox_enabled", "policy_checked", "audit_log"])
    assert rep.valid is True


def test_toolchain_safety_violation():
    rep = ToolchainSafetyVerifier().verify(["sandbox_enabled"])
    assert rep.valid is False
    assert "policy_checked" in rep.violated_rules
