from novacore.models.self_learning import SelfLearningController


def test_self_learning_reinforce_and_forget():
    s = SelfLearningController(decay=0.1)
    s.reinforce("planning", 0.3)
    before = s.state().strengths["planning"]
    s.controlled_forgetting()
    after = s.state().strengths["planning"]
    assert after <= before
    assert after >= 0.1
