from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class OnlineObservation:
    text: str
    image_regions: int
    tool_events: int


@dataclass
class OnlineStepResult:
    action: str
    success: bool
    note: str


class MultimodalOnlineAgent:
    """Онлайн-агент, що приймає стрім спостережень і видає дії."""

    def __init__(self) -> None:
        self.history: List[OnlineObservation] = []

    def observe(self, text: str, image_regions: int = 0, tool_events: int = 0) -> OnlineObservation:
        obs = OnlineObservation(text=text, image_regions=image_regions, tool_events=tool_events)
        self.history.append(obs)
        return obs

    def act(self, policy_hint: str = "analyze") -> OnlineStepResult:
        if not self.history:
            return OnlineStepResult("idle", False, "no_observation")
        last = self.history[-1]
        if "danger" in last.text.lower():
            return OnlineStepResult("halt", True, "safety_trigger")
        if last.tool_events > 0:
            return OnlineStepResult("tool_verify", True, "tool_path")
        return OnlineStepResult(policy_hint, True, "normal_path")

    def snapshot(self) -> Dict[str, int]:
        return {
            "observations": len(self.history),
            "total_regions": sum(x.image_regions for x in self.history),
            "total_tool_events": sum(x.tool_events for x in self.history),
        }
