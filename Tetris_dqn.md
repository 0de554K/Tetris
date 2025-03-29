# Project: DQN-Based Tetris Agent

##  Problem Statement
The goal was to implement an AI agent capable of playing Tetris autonomously using reinforcement learning. The initial version of the agent was based on tabular Q-learning, which quickly became limited due to the complexity and dimensionality of the Tetris state space. A more scalable and generalizable solution was needed.

##  Steps Taken

1. **Refactored Game Architecture**
   - Separated `TetrisAI` and `AppAI` classes to allow AI integration without modifying the base game.
   - Ensured that AI-specific logic is encapsulated and cleanly extendable.

2. **Implemented QAgent (Tabular)**
   - Created a simple `QAgent` for proof of concept using ε-greedy exploration.
   - Connected it to the game loop and verified it could interact with the environment.

3. **Replaced QAgent with DQNAgent**
   - Implemented a PyTorch-based deep Q-network (`DQN`) and `DQNAgent`.
   - The state vector includes column heights and one-hot encoding of the current tetromino.
   - Rewards are based on score deltas.

4. **Added Replay Buffer**
   - Enabled the agent to learn from past transitions using mini-batches.
   - Improves stability and breaks correlation between sequential game states.

5. **Implemented Model Persistence**
   - The agent automatically saves and loads its neural network from disk (`dqn_model.pth`).

6. **Introduced Learning Metrics and Visualization**
   - Scores, rewards, and ε (exploration rate) are logged after each game.
   - A `plot_learning_curve()` method visualizes progress and opens a GUI graph on exit.

## Purpose of These Steps

- **Scalability**: Deep learning handles complex state spaces better than tabular Q-learning.
- **Stability**: Replay buffer and mini-batch training reduce noise in updates.
- **Reproducibility**: Saving and loading models makes training incremental.
- **Transparency**: Graphs provide visual feedback about learning progress.

## Current Status

- The DQN agent is fully integrated and trains in real-time.
- It retains learned behavior across sessions.
- It generates and displays a live learning curve upon game exit.
- No major runtime errors persist, and training is stable.

## Next Steps for Improvement

1. **Improve State Representation**
   - Include features like holes, bumpiness, aggregate height, etc.

2. **Add Target Network**
   - To stabilize Q-learning updates, maintain a separate target model.

3. **Implement Reward Shaping**
   - Tune the reward system (e.g., penalize for height, reward for clearing rows).

4. **Add Episode Management**
   - Track episode boundaries more explicitly for training/plotting.

5. **Support Faster Training**
   - Headless training mode (no rendering) to run large batches.