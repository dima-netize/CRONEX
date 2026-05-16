from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ToolPolicy:
    allow_tool_add: bool


class ToolSandbox:
    def policy_for_mode(self, governance_mode: str) -> ToolPolicy:
        if governance_mode == "halt":
            return ToolPolicy(allow_tool_add=False)
        if governance_mode == "cautious":
            return ToolPolicy(allow_tool_add=False)
        return ToolPolicy(allow_tool_add=True)
