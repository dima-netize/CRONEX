from novacore.models.agi_readiness import estimate_agi_readiness


if __name__ == "__main__":
    score = estimate_agi_readiness(
        has_working_memory=True,
        has_branching=True,
        has_verifier=True,
        has_tool_use=True,
        has_learned_repair=True,
    )

    print("AGI readiness (prototype-level):")
    print(f"- memory_score={score.memory_score}")
    print(f"- planning_score={score.planning_score}")
    print(f"- verification_score={score.verification_score}")
    print(f"- tool_use_score={score.tool_use_score}")
    print(f"- adaptation_score={score.adaptation_score}")
    print(f"- overall={score.overall}")
