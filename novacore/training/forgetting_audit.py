from __future__ import annotations

from novacore.models.novacore import NovaCoreMini

BASE = [
    "STORE_COLOR C1 | SHIFT N2 | QUERY",
    "PAIR S1 C5 | QUERY S1",
    "TOOL_ADD 7 8 SUM | QUERY SUM",
]
NEW = [
    "STORE_COLOR C2 | REPEAT 15 SHIFT N1 | QUERY",
    "TOOL_ADD 20 22 SUM | QUERY SUM",
]


def score(model: NovaCoreMini, data: list[str]) -> float:
    ok = 0
    for p in data:
        out = model.run(p)
        ok += int(out.verified)
    return ok / len(data)


if __name__ == "__main__":
    model = NovaCoreMini(max_retries=1)
    before = score(model, BASE)

    # simulate learning new tasks
    for p in NEW:
        model.run(p)

    after = score(model, BASE)
    degradation = max(0.0, before - after)

    print(f"before={before:.4f}")
    print(f"after={after:.4f}")
    print(f"degradation={degradation:.4f}")

    if degradation > 0.02:
        raise SystemExit("FAIL: catastrophic forgetting degradation > 2%")
