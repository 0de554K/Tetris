from tetris_ai import TetrisAI


def test_tetris_ai_initializes(dummy_app):
    tetris = TetrisAI(dummy_app)
    assert tetris.agent is not None
    assert hasattr(tetris, 'control')
    assert hasattr(tetris, 'update')

def test_tetris_ai_control_calls_agent(monkeypatch, dummy_app):
    tetris = TetrisAI(dummy_app)
    actions = []

    def fake_choose_action(state):
        actions.append(state)
        return 'left'

    tetris.agent.choose_action = fake_choose_action
    tetris.control()
    assert actions