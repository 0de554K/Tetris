import pytest
from tetris_ai import QAgent, TetrisAI

def test_qagent_returns_default_q():
    agent = QAgent()
    assert agent.q.get(('nonexistent', 'action'), 0.0) == 0.0
    assert agent.get_state(type('Tetris', (), {'tetromino': type('Tetromino', (), {'shape': 'O'})})) == 'O'

def test_qagent_choose_between_equal_q(monkeypatch):
    agent = QAgent(epsilon=0.0)
    agent.q = {
        ('state', 'left'): 1.0,
        ('state', 'right'): 1.0,
        ('state', 'rotate'): 1.0,
        ('state', 'down'): 1.0,
    }
    action = agent.choose_action('state')
    assert action in agent.actions

def test_tetrisai_control_only_on_timer(dummy_app):
    tetris = TetrisAI(dummy_app)
    tetris.agent_timer = 0
    tetris.speed_up = False
    dummy_app.anim_trigger = True
    tetris.update()
    assert tetris.agent_timer == 1

@pytest.mark.skip(reason="For now")
def test_tetris_game_not_over_at_start(dummy_app):
    tetris = TetrisAI(dummy_app)
    assert not tetris.is_game_over()

def test_check_full_lines_empty_field(dummy_app):
    tetris = TetrisAI(dummy_app)
    initial_score = tetris.score
    tetris.check_full_lines()
    assert tetris.score == initial_score
