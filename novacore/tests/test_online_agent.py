from novacore.models.online_agent import MultimodalOnlineAgent


def test_online_agent_observe_and_act():
    agent = MultimodalOnlineAgent()
    agent.observe("normal update", image_regions=2, tool_events=1)
    res = agent.act()
    assert res.success is True
    assert res.action in {"tool_verify", "analyze"}


def test_online_agent_safety_halt():
    agent = MultimodalOnlineAgent()
    agent.observe("danger detected")
    res = agent.act()
    assert res.action == "halt"
