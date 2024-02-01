#### Overview: Reinforcement Learning in Game Theory
In Lab 10, Reinforcement Learning (RL) is applied to the game of Tic-Tac-Toe. RL, particularly suited for strategic game.

#### Q-Learning: Theoretical Framework
- **Core Concept:** Q-learning, a model-free RL algorithm, allows an agent to learn the value of actions in states, maximizing rewards.
- **Q-Table:** Stores Q-values, representing the expected utility of actions in each state.
- **Bellman Equation for Updates:** Q-values are iteratively updated. An example update for player X's action is as follows:
  
  
\[ Q(s, a) \leftarrow Q(s, a) + \alpha \left( r + \gamma \max_{a'} Q(s', a') - Q(s, a) \right) \]

Where:
- \( Q(s, a) \) is the Q-value of the current state-action pair.
- \( \alpha \) is the learning rate.
- \( r \) is the immediate reward received after taking action \( a \) in state \( s \).
- \( \gamma \) is the discount factor.
- \( \max_{a'} Q(s', a') \) is the maximum predicted Q-value for the next state \( s' \), representing the best expected future rewards.

#### Key Components of the Code
1. **Q-Table Initialization (`initialize_Q` Function):**
   - Initializes Q-tables for each state in the game, storing state-action values.
   - Random values are assigned initially, enabling exploration.

2. **Tic-Tac-Toe Board Setup:**
   - Two TicTacToe board instances are created for players X and O with specified reward types.

3. **Training Function (`train`):**
   - Trains the agents for a specified number of games using Q-learning.
   - Learning rate (`alpha`) and discount factor (`gamma`) determine the Q-value update.
   - Training alternates between players X and O, controlled by flags `train_X` and `train_O`.

4. **Q-Value Update:**
   - The Q-table is updated using a formula incorporating the immediate reward and discounted future rewards.
   - The update rule is: `Q[state][action] += alpha * (reward + gamma * max(Q[new_state]) - Q[state][action])`.

5. **Gameplay Simulation (`play_games` Function):**
   - Simulates a specified number of games, recording win statistics and game sequences.
   - Players can adopt either an epsilon-greedy or greedy strategy based on Q-tables.

6. **Winning Statistics Analysis (`get_win_statistics`):**
   - Compiles winning statistics over multiple sets of games.
   - Generates insights on winning sequences, first move statistics, and win rates.

7. **Result Visualization (`plot_results` Function):**
   - Visualizes game outcomes, win rates, and distributions using seaborn plots.

#### Implementation Details
- The RL model alternates training between players X and O to balance the learning process.
- Epsilon-greedy and greedy strategies dictate the players' moves, balancing exploration and exploitation.
- The model's performance is evaluated by pitting trained agents against each other and against random strategies.