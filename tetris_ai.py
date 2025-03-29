from tetris import Tetris
from base_app_class import App
from settings import pg

import sys
import random

class QAgent:
    def __init__(self, epsilon=0.1):
        self.epsilon = epsilon
        self.q = {}  # (state, action) -> value
        self.actions = ['left', 'right', 'rotate', 'down']

    def get_state(self, tetris):
        return tetris.tetromino.shape

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        return random.choice(self.actions)  # No learning yet

    def update(self, *args):
        pass


class TetrisAI(Tetris):
    def __init__(self, app):
        super().__init__(app)
        self.agent = QAgent()
        self.agent_timer = 0

    def control(self, pressed_key=None):
        state = self.agent.get_state(self)
        action = self.agent.choose_action(state)
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
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()
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