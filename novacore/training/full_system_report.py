from novacore.models.agi_maturity import classify_maturity
from novacore.models.agi_readiness import estimate_agi_readiness
from novacore.models.metrics import compute_metrics
from novacore.models.novacore import NovaCoreMini


DATASET = [
    "STORE_COLOR C4 | SHIFT N2 | SHIFT N3 | QUERY",
    "PAIR S3 C7 | QUERY S3",
    "PAIR S3 C7 | QUERY C7",
    "STORE_COLOR C1 | REPEAT 3 SHIFT N1 | QUERY",
    "TOOL_ADD 4 5 SUM | QUERY SUM",
    "DELETE_ALL | QUERY",
]

if __name__ == "__main__":
    model = NovaCoreMini(max_retries=1)
    model.learn_runtime_rule("MOVE", "SHIFT N2")

    verified = 0
    retries_sum = 0
    for p in DATASET:
        out = model.run(p)
        verified += int(out.verified)
        retries_sum += out.retries_used
        print(f"{p} => ok={out.verified} mode={out.governance_mode} drift={out.drift_score}")

    m = compute_metrics(total=len(DATASET), verified=verified, retries_sum=retries_sum)
    readiness = estimate_agi_readiness(True, True, True, True, True)
    maturity = classify_maturity(readiness.overall)

    print("\n=== SYSTEM REPORT ===")
    print(f"task_accuracy={m.accuracy}")
    print(f"avg_retries={m.avg_retries}")
    print(f"readiness_overall={readiness.overall}")
    print(f"maturity_level={maturity.level}")
    print(f"maturity_note={maturity.interpretation}")
