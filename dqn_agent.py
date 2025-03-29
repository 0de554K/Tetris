import torch
import torch.nn as nn
import torch.optim as optim
import random
import os
from collections import deque
import matplotlib.pyplot as plt

MODEL_PATH = "dqn_model.pth"

class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, output_dim)
        )

    def forward(self, x):
        return self.layers(x)


class DQNAgent:
    def __init__(self, state_dim, action_list, gamma=0.99, lr=1e-3, epsilon=1.0, epsilon_min=0.1, epsilon_decay=0.995, buffer_size=10000, batch_size=64):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DQN(state_dim, len(action_list)).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.criterion = nn.MSELoss()
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.actions = action_list

        self.buffer = deque(maxlen=buffer_size)
        self.batch_size = batch_size

        self.episode_rewards = []
        self.episode_scores = []
        self.episode_epsilons = []

        self.load_model()

    def get_state(self, tetris):
        heights = [0] * 10
        for x in range(10):
            for y in range(20):
                if tetris.field_array[y][x]:
                    heights[x] = 20 - y
                    break
        shape_index = [0] * 7
        shapes = list("TOJLIZS")
        shape_index[shapes.index(tetris.tetromino.shape)] = 1
        return torch.tensor(heights + shape_index, dtype=torch.float32).to(self.device)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        with torch.no_grad():
            q_vals = self.model(state.unsqueeze(0))
            return self.actions[torch.argmax(q_vals).item()]

    def remember(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def replay(self):
        if len(self.buffer) < self.batch_size:
            return
        batch = random.sample(self.buffer, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.stack(states)
        next_states = torch.stack(next_states)
        rewards = torch.tensor(rewards, dtype=torch.float32, device=self.device)
        dones = torch.tensor(dones, dtype=torch.bool, device=self.device)

        q_vals = self.model(states)
        next_q_vals = self.model(next_states).detach()

        target_q_vals = q_vals.clone().detach()
        for i, action in enumerate(actions):
            action_idx = self.actions.index(action)
            target = rewards[i]
            if not dones[i]:
                target += self.gamma * torch.max(next_q_vals[i])
            target_q_vals[i, action_idx] = target

        loss = self.criterion(q_vals, target_q_vals)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def log_episode(self, score, reward):
        self.episode_scores.append(score)
        self.episode_rewards.append(reward)
        self.episode_epsilons.append(self.epsilon)

    def plot_learning_curve(self, show=False):
        if not self.episode_scores:
            return
        plt.figure(figsize=(10, 6))
        plt.plot(self.episode_scores, label='Score per Episode')
        plt.plot(self.episode_rewards, label='Reward per Episode')
        plt.plot(self.episode_epsilons, label='Epsilon')
        plt.xlabel('Episodes')
        plt.ylabel('Value')
        plt.legend()
        plt.title('DQN Learning Progress')
        plt.grid()
        plt.tight_layout()
        plt.savefig('learning_curve.png')
        if show:
            plt.show()
        plt.close()

    def save_model(self):
        torch.save(self.model.state_dict(), MODEL_PATH)

    def load_model(self):
        if os.path.exists(MODEL_PATH):
            self.model.load_state_dict(torch.load(MODEL_PATH, map_location=self.device))
            self.model.eval()
            print(f"Loaded model from {MODEL_PATH}")
