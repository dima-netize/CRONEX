from __future__ import annotations

from novacore.models.novacore import NovaCoreMini


def run_program(model: NovaCoreMini, steps: int):
    # compact long-horizon encoding via REPEAT avoids safety string-length gating
    p = f"STORE_COLOR C1 | REPEAT {steps} SHIFT N1 | QUERY"
    return model.run(p)


if __name__ == "__main__":
    model = NovaCoreMini(max_retries=1)
    steps_list = [500, 1000, 1500]
    passed = 0
    total = len(steps_list)
    cost_budget = 2000

    for s in steps_list:
        out = run_program(model, s)
        completion = out.verified and out.governance_mode == "normal"
        safety_preserved = out.governance_mode != "halt"
        cost_ok = s <= cost_budget
        passed += int(completion and safety_preserved and cost_ok)
        print(f"steps={s} completion={completion} safety={safety_preserved} cost_ok={cost_ok} answer={out.answer}")

    print(f"\ncompletion_rate={round(passed/total,4)}")
