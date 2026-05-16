from novacore.models.metrics import compute_metrics
from novacore.models.novacore import NovaCoreMini


CURRICULUM = {
    "easy": [
        "STORE_COLOR C1 | QUERY",
        "STORE_COLOR C2 | SHIFT N1 | QUERY",
    ],
    "medium": [
        "PAIR S3 C7 | QUERY S3",
        "STORE_COLOR C1 | REPEAT 3 SHIFT N1 | QUERY",
    ],
    "hard": [
        "TOOL_ADD 4 5 SUM | QUERY SUM",
        "STORE_COLOR C1 | MOVE | QUERY",  # requires runtime adaptation
    ],
}


if __name__ == "__main__":
    model = NovaCoreMini(max_retries=1)
    model.learn_runtime_rule("MOVE", "SHIFT N2")

    total = verified = retries_sum = 0
    for level, programs in CURRICULUM.items():
        print(f"\n[{level}]")
        for p in programs:
            out = model.run(p)
            total += 1
            verified += int(out.verified)
            retries_sum += out.retries_used
            print(f"{p} => ans={out.answer} ok={out.verified} mode={out.governance_mode}")

    m = compute_metrics(total=total, verified=verified, retries_sum=retries_sum)
    print(f"\nTOTAL: accuracy={m.accuracy}, avg_retries={m.avg_retries}")
