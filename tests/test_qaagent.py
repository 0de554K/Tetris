from tetris_ai import QAgent

def test_qagent_get_state(dummy_tetris):
    agent = QAgent()
    dummy = dummy_tetris
    state = agent.get_state(dummy)
    assert state == 'T'

def test_qagent_choose_action_random(monkeypatch):
    agent = QAgent(epsilon=1.0)  # force exploration
    monkeypatch.setattr('random.choice', lambda x: 'rotate')
    assert agent.choose_action('any_state') == 'rotate'