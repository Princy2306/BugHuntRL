# 🐞 BugHuntRL
### An RL Agent That Learns to Break Software Efficiently

BugHuntRL is a reinforcement learning mini-project that explores how an intelligent agent can discover software bugs and improve code coverage under a limited testing budget.

The project integrates a **Proximal Policy Optimization (PPO)** agent with a testing engine and compares its performance against conventional testing strategies. An interactive Streamlit dashboard visualizes the experimental results.

## 🎯 Objectives

- Discover previously unknown software bugs efficiently.
- Improve code coverage within a fixed testing budget.
- Learn adaptive testing strategies using reinforcement learning.
- Compare PPO against fixed testing strategies.
- Visualize performance through an interactive dashboard.

## ⚙️ How It Works

1. **Observe:** The agent receives the remaining budget, coverage, bugs found, tests executed, and recent success rate.
2. **Choose:** It selects one of four testing strategies.
3. **Execute:** The testing engine runs the selected strategy against the target application.
4. **Reward:** The environment evaluates bug discoveries, coverage gains, redundant tests, and testing cost.
5. **Learn:** PPO learns a policy for selecting testing strategies across episodes.

## 🧠 Reinforcement Learning Formulation

- **State space:** Five observations—remaining budget, coverage fraction, unique bugs found, tests executed, and recent success rate.
- **Action space:** Four discrete testing strategies:

| Action | Strategy | Cost |
|---|---|---:|
| 0 | Random testing | 5 |
| 1 | Boundary-value testing | 8 |
| 2 | Input mutation | 6 |
| 3 | Sequence generation | 10 |

- **Reward function:**

  `R = 10 × new_bugs + 5 × coverage_gain − 2 × redundant − 0.1 × cost`

- **Algorithm:** Proximal Policy Optimization (PPO), implemented using Stable-Baselines3.
- **Environment:** Gymnasium environment connected to the project's `TestingEngine`.
- **Budget:** 100 units per episode.

## 📊 Evaluation Results

The project evaluates four fixed testing strategies and a PPO agent. The current experiment uses 20 runs per baseline strategy and 20 PPO evaluation episodes.

| Metric | PPO result |
|---|---:|
| Average reward | 6.34 |
| Average unique bugs found | 3.00 |
| Average coverage | 88.89% |
| Average budget used | 91 units |
| Average budget remaining | 9 units |

The fixed-strategy baselines achieved the following averages:

| Baseline strategy | Average bugs | Average coverage | Average budget used |
|---|---:|---:|---:|
| Random testing | 3.00 | 88.89% | 100 |
| Boundary-value testing | 3.00 | 88.89% | 96 |
| Input mutation | 1.00 | 66.67% | 96 |
| Sequence generation | 3.00 | 88.89% | 100 |

**Interpretation:** In this experiment, PPO discovered an average of three unique bugs and achieved 88.89% coverage while using an average of 91 budget units. These results are preliminary and do not establish that PPO is universally better than fixed strategies.

The experiments use a controlled target application. Further testing across more applications and varied seeds would be needed to assess generalization.

### Evaluation files

Results and generated charts are stored in `results/`:

- `strategy_results.csv` — fixed-strategy baseline results
- `ppo_evaluation_results.csv` — per-episode PPO results
- `baseline_results.csv` and `ppo_results.csv` — additional result files
- `bugs_comparison.html` — bug discovery comparison
- `coverage_comparison.html` — coverage comparison
- `execution_time_comparison.html` — execution-time comparison

## 📈 Interactive Dashboard

The Streamlit dashboard compares baseline strategies and PPO using charts, summary metrics, and a results table.

Launch it from the project root:

```bash
python -m streamlit run dashboard/app.py
```

## 📁 Project Structure

```text
BugHuntRL/
├── src/
│   ├── __init__.py
│   ├── bughunt_engine_env.py
│   ├── bughunt_env.py
│   ├── sample_app.py
│   └── testing_engine.py
├── scripts/
│   ├── train_agent.py
│   ├── evaluate_ppo.py
│   ├── evaluate_baseline.py
│   ├── evaluate_testing_strategies.py
│   └── plot_strategy_results.py
├── tests/
│   ├── test_bughunt_engine_env.py
│   ├── test_sample_app_coverage.py
│   ├── test_strategies.py
│   └── test_testing_engine.py
├── dashboard/
│   └── app.py
├── models/
│   └── bughunt_engine_ppo.zip
├── archive/
│   ├── bughunt_engine_ppo_backup.zip
│   ├── bughunt_ppo_initial.zip
│   └── bughunt_ppo_updated.zip
├── results/
├── requirements.txt
├── README.md
└── .gitignore
```

## 🚀 Getting Started

### 1. Clone the repository

Replace the placeholder URL with your actual GitHub repository URL.

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd BugHuntRL
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

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
python -m pip install -r requirements.txt
```

### 4. Run the tests

```bash
python -m pytest -q
```

### 5. Launch the dashboard

```bash
python -m streamlit run dashboard/app.py
```

### 6. Run evaluations

From the project root:

```bash
python -m scripts.evaluate_testing_strategies
python -m scripts.evaluate_ppo
```

**Note:** These evaluation scripts write their results to `results/`. Running them again will overwrite the corresponding CSV files.

### 7. Train a new PPO model

```bash
python -m scripts.train_agent
```

The training script saves a new checkpoint to `models/bughunt_engine_ppo_new.zip`, preserving the current checkpoint.

## 🛠️ Technology Stack

- **Python** — Core implementation
- **Gymnasium** — Reinforcement learning environment
- **Stable-Baselines3 and PyTorch** — PPO implementation and training
- **pytest** — Automated testing
- **coverage.py** — Code coverage measurement
- **Streamlit and Plotly** — Interactive dashboard

## 👥 Contributors

- [Shreya Sardar](https://github.com/shreyasardar)
- [Princy Nimmagadda](https://github.com/Princy2306)

## 🎓 Project Information

Reinforcement Learning Mini-Project — Assignment 2

Developed for academic purposes using a controlled software-testing environment.

## 📜 License

No license has been specified yet.
