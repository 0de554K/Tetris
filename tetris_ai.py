from tetris import Tetris
from base_app_class import App
from settings import pg
from dqn_agent import DQNAgent

import sys
import logging

logger = logging.getLogger("DQNAgent")

class TetrisAI(Tetris):
    def __init__(self, app):
        super().__init__(app)
        self.agent = DQNAgent(state_dim=17, action_list=['left', 'right', 'rotate', 'down'])
        self.agent_timer = 0
        self.last_state = None
        self.last_action = None
        self.episode_reward = 0

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
            self.episode_reward += reward

            if self.last_state is not None and self.last_action is not None:
                next_state = self.agent.get_state(self)
                done = self.is_game_over() or self.tetromino.landing
                self.agent.remember(self.last_state, self.last_action, reward, next_state, done)
                self.agent.replay()

            if self.is_game_over():
                self.agent.log_episode(self.score, self.episode_reward)
                self.episode_reward = 0

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
                self.tetris.agent.save_model()
                self.tetris.agent.plot_learning_curve(show=True)
                pg.quit()
                sys.exit()
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True
