# BugHuntRL
### An RL Agent That Learns to Break Software Efficiently

BugHuntRL is a reinforcement learning mini-project that explores how an intelligent agent can discover software bugs and improve code coverage while operating under a limited testing budget.

Instead of relying entirely on random testing, the agent learns to select testing strategies based on previous outcomes, newly explored code, discovered failures, and remaining resources.

## Objectives

- Discover previously unknown software bugs efficiently.
- Maximize code coverage within a fixed testing budget.
- Learn adaptive testing strategies using reinforcement learning.
- Compare the RL agent against conventional testing baselines.
- Visualize testing progress and performance through an interactive dashboard.

## How It Works

1. **Observe:** The agent receives information about code coverage, past testing results, discovered bugs, and remaining budget.
2. **Choose:** It selects a testing strategy, such as random testing, boundary-value testing, or input mutation.
3. **Execute:** The selected strategy generates and executes test inputs against the target program.
4. **Reward:** The agent receives feedback based on new coverage, newly discovered bugs, and testing costs.
5. **Learn:** The agent improves its decisions over repeated testing episodes.


## Reinforcement Learning Formulation

- **State Space:** A five-value observation containing remaining testing budget, coverage fraction, unique bugs found, tests executed, and recent test success rate.
- **Action Space:** Four discrete testing strategies:
  - `0` — Random testing (cost: 5 budget units)
  - `1` — Boundary-value testing (cost: 8 budget units)
  - `2` — Input mutation (cost: 6 budget units)
  - `3` — Sequence generation (cost: 10 budget units)
- **Reward Function:** `R = 10 × new_bugs + 5 × coverage_gain − 2 × redundant − 0.1 × cost`
  - Rewards new bug discoveries and coverage gains.
  - Penalizes tests that discover neither bugs nor coverage, and accounts for testing cost.
- **Environment:** A Gymnasium-based simulator with a budget of 100 units and shared pools of 20 potential bugs and 20 coverage units.
- **Algorithm:** Proximal Policy Optimization (PPO), implemented using Stable-Baselines3.
- **Episode Termination:** An episode ends when the remaining budget falls below 5 units or the selected strategy cannot be afforded.
- **Current Limitation:** Outcomes are simulated. Integration with the real testing pipeline and validation on actual software remain pending.


## Technology Stack

- Python — Core implementation
- Gymnasium — RL environment
- Stable-Baselines3 / PyTorch — Agent training, if selected
- pytest — Test execution
- Hypothesis — Property-based input generation
- coverage.py — Code coverage measurement
- Streamlit and Plotly — Interactive visualization

## Evaluation

The RL agent will be evaluated against baseline testing strategies using comparable testing budgets.

Planned metrics:
- Number of unique bugs discovered
- Code coverage achieved
- Number of tests executed
- Execution cost
- Performance across repeated runs

Experimental results and visualizations will be added after evaluation.

## 📁 Project Structure

```text
BugHuntRL/
├── src/
│   ├── environment.py
│   ├── agent.py
│   ├── testing_engine.py
│   └── reward.py
├── tests/
├── experiments/
├── dashboard/
│   └── app.py
├── models/
├── results/
├── requirements.txt
├── README.md
└── .gitignore
```

The structure may evolve during implementation.

## Getting Started

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd BugHuntRL
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**macOS / Linux**
```bash
source .venv/bin/activate
```

**Windows**
```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Execution commands will be finalized as the implementation becomes available.

## 👥 Contributors

- [Shreya Sardar](https://github.com/shreyasardar)
- [Princy Nimmagadda](https://github.com/Princy2306)

## 🎓 Project Information

Reinforcement Learning Mini-Project — Assignment 2

The project is developed for academic purposes and uses a controlled testing environment.

## 📜 License

To be decided.
