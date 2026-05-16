from __future__ import annotations

from novacore.models.novacore import NovaCoreMini


def build_long_program(steps: int) -> str:
    parts = ["STORE_COLOR C1"]
    parts.extend(["SHIFT N1"] * steps)
    parts.append("QUERY")
    return " | ".join(parts)


if __name__ == "__main__":
    model = NovaCoreMini(max_retries=1)
    program = build_long_program(steps=300)
    out = model.run(program)
    print(f"steps=300 ok={out.verified} mode={out.governance_mode} horizon={out.horizon_reason} answer={out.answer}")
