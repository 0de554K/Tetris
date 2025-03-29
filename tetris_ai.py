from tetris import Tetris
from base_app_class import App
from settings import pg

import sys
import random
import logging

logger = logging.getLogger("QAgent")

class QAgent:
    def __init__(self, alpha=0.1, gamma=0.95, epsilon=0.1):
        self.q = {}  # (state, action) -> value
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.actions = ['left', 'right', 'rotate', 'down']

    def get_q(self, state, action):
        return self.q.get((state, action), 0.0)

    def get_state(self, tetris):
        return tetris.tetromino.shape

    def choose_action(self, state):
        if random.random() < self.epsilon:
            action = random.choice(self.actions)
            logger.info(f"[explore] state={state}, action={action}")
            return action
        # Exploit
        q_vals = {a: self.get_q(state, a) for a in self.actions}
        max_q = max(q_vals.values())
        best_actions = [a for a, q in q_vals.items() if q == max_q]
        action = random.choice(best_actions)
        logger.info(f"[exploit] state={state}, action={action}, q={max_q}")
        return action

    def update(self, state, action, reward, next_state):
        max_next_q = max([self.get_q(next_state, a) for a in self.actions], default=0.0)
        current_q = self.get_q(state, action)
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q[(state, action)] = new_q
        logger.info(f"Updated Q[{state}, {action}] = {new_q:.3f}")


class TetrisAI(Tetris):
    def __init__(self, app):
        super().__init__(app)
        self.agent = QAgent()
        self.agent_timer = 0
        self.last_state = None
        self.last_action = None

    def control(self, pressed_key=None):
        state = self.agent.get_state(self)
        action = self.agent.choose_action(state)
        self.last_state = state
        self.last_action = action

        if action == 'left':
            self.tetromino.move('left')
        elif action == 'right':
            self.tetromino.move('right')
        elif action == 'rotate':
            self.tetromino.rotate()
        elif action == 'down':
            self.speed_up = True

    def update(self):
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.agent_timer += 1
            if self.agent_timer >= 5:
                self.control()
                self.agent_timer = 0

            prev_score = self.score
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()
            reward = self.score - prev_score

            if self.last_state and self.last_action:
                next_state = self.agent.get_state(self)
                self.agent.update(self.last_state, self.last_action, reward, next_state)
        self.sprite_group.update()


class AppAI(App):
    def __init__(self):
        super().__init__()
        self.tetris = TetrisAI(self)

    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True