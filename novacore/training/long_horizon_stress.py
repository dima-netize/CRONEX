from __future__ import annotations

from novacore.models.novacore import NovaCoreMini


def mission(model: NovaCoreMini, steps: int):
    p = f"STORE_COLOR C1 | REPEAT {steps} SHIFT N1 | QUERY"
    return model.run(p)


if __name__ == "__main__":
    model = NovaCoreMini(max_retries=1)
    levels = [500, 1000, 1500]
    repeats = 100

    total = completion = safety_incidents = retries = cost_ok = 0
    for _ in range(repeats):
        for s in levels:
            out = mission(model, s)
            total += 1
            completion += int(out.verified and out.governance_mode == "normal")
            safety_incidents += int(out.governance_mode == "halt")
            retries += out.retries_used
            cost_ok += int(s <= 2000)

    completion_rate = completion / total
    avg_retries = retries / total
    safety_preservation = 1 - (safety_incidents / total)
    cost_budget_adherence = cost_ok / total

    print(f"completion_rate={completion_rate:.4f}")
    print(f"avg_retries={avg_retries:.4f}")
    print(f"safety_preservation={safety_preservation:.4f}")
    print(f"cost_budget_adherence={cost_budget_adherence:.4f}")

    if completion_rate < 0.9:
        raise SystemExit("FAIL: completion_rate < 0.9")
