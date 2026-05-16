from novacore.models.replay import ExperienceReplayStore


def test_replay_success_rate_and_capacity():
    r = ExperienceReplayStore(capacity=3)
    r.add("a", True)
    r.add("b", False)
    r.add("c", True)
    r.add("d", True)
    assert len(r.items) == 3
    assert round(r.success_rate(), 4) == round(2/3, 4)
