from novacore.models.metrics import compute_metrics
from novacore.models.novacore import NovaCoreMini


DATASET = [
    "STORE_COLOR C4 | SHIFT N2 | SHIFT N3 | QUERY",
    "PAIR S3 C7 | QUERY S3",
    "PAIR S3 C7 | QUERY C7",
    "STORE_COLOR C1 | QUERY",
    "QUERY",
]


if __name__ == "__main__":
    model = NovaCoreMini(max_retries=1)

    verified = 0
    retries_sum = 0
    for program in DATASET:
        out = model.run(program)
        verified += int(out.verified)
        retries_sum += out.retries_used
        print(f"{program} => answer={out.answer} verified={out.verified} retries={out.retries_used}")

    metrics = compute_metrics(total=len(DATASET), verified=verified, retries_sum=retries_sum)
    print("\n=== Metrics ===")
    print(f"total={metrics.total}")
    print(f"verified={metrics.verified}")
    print(f"accuracy={metrics.accuracy}")
    print(f"avg_retries={metrics.avg_retries}")
