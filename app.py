
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="BugHuntRL Dashboard",
    page_icon="🐞",
    layout="wide",
)

st.title("🐞 BugHuntRL — Testing Strategy Dashboard")
st.write(
    "Compare fixed testing strategies with a PPO reinforcement "
    "learning agent using bug detection, code coverage, time, "
    "and budget usage."
)

BASELINE_FILE = "strategy_results.csv"
PPO_FILE = "ppo_evaluation_results.csv"

# Load baseline results
try:
    baseline_df = pd.read_csv(BASELINE_FILE)
except FileNotFoundError:
    st.error(
        f"{BASELINE_FILE} not found. "
        "Run evaluate_testing_strategies.py first."
    )
    st.stop()

baseline_required = {
    "strategy",
    "run",
    "unique_bugs_found",
    "coverage_percent",
    "execution_time_seconds",
    "budget_used",
}

missing = baseline_required - set(baseline_df.columns)

if missing:
    st.error(
        f"{BASELINE_FILE} is missing columns: "
        f"{', '.join(sorted(missing))}. "
        "Run the updated evaluate_testing_strategies.py."
    )
    st.stop()

baseline_df["method_type"] = "Baseline"

# Load PPO results
try:
    ppo_df = pd.read_csv(PPO_FILE)
except FileNotFoundError:
    ppo_df = None
    st.warning(
        f"{PPO_FILE} not found. Showing baseline results only. "
        "Run evaluate_ppo.py to generate PPO results."
    )

if ppo_df is not None:
    ppo_required = {
        "episode",
        "unique_bugs_found",
        "coverage_percent",
        "budget_used",
        "total_reward",
    }

    missing = ppo_required - set(ppo_df.columns)

    if missing:
        st.error(
            f"{PPO_FILE} is missing columns: "
            f"{', '.join(sorted(missing))}."
        )
        st.stop()

    ppo_df["strategy"] = "PPO Agent"
    ppo_df["run"] = ppo_df["episode"]
    ppo_df["method_type"] = "Reinforcement Learning"

    # PPO evaluation currently does not record execution time.
    ppo_df["execution_time_seconds"] = float("nan")

    # The baseline and PPO files use different cost definitions.
    # Preserve budget_used as the common budget metric.
    if "execution_cost" not in ppo_df.columns:
        ppo_df["execution_cost"] = float("nan")

    common_columns = [
        "strategy",
        "run",
        "unique_bugs_found",
        "coverage_percent",
        "execution_time_seconds",
        "budget_used",
        "method_type",
    ]

    df = pd.concat(
        [
            baseline_df[common_columns],
            ppo_df[common_columns],
        ],
        ignore_index=True,
    )
else:
    df = baseline_df.copy()

st.subheader("Experiment Overview")

summary = (
    df.groupby(["strategy", "method_type"], as_index=False)
    .agg(
        average_bugs=("unique_bugs_found", "mean"),
        average_coverage=("coverage_percent", "mean"),
        average_time=("execution_time_seconds", "mean"),
        average_budget=("budget_used", "mean"),
        runs=("run", "count"),
    )
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Methods Compared", summary["strategy"].nunique())
col2.metric("Total Runs / Episodes", len(df))
col3.metric(
    "Average Unique Bugs",
    f"{df['unique_bugs_found'].mean():.2f}",
)
col4.metric(
    "Average Coverage",
    f"{df['coverage_percent'].mean():.2f}%",
)

st.divider()

st.subheader("Strategy Comparison")

metric = st.selectbox(
    "Choose a metric",
    [
        "Average Unique Bugs",
        "Average Code Coverage (%)",
        "Average Budget Used",
        "Average Execution Time (seconds)",
    ],
)

metric_columns = {
    "Average Unique Bugs": (
        "average_bugs",
        "Average unique bugs found",
    ),
    "Average Code Coverage (%)": (
        "average_coverage",
        "Coverage (%)",
    ),
    "Average Budget Used": (
        "average_budget",
        "Budget units used",
    ),
    "Average Execution Time (seconds)": (
        "average_time",
        "Execution time (seconds)",
    ),
}

column, y_label = metric_columns[metric]

fig = px.bar(
    summary,
    x="strategy",
    y=column,
    color="method_type",
    barmode="group",
    text=column,
    title=metric,
    labels={
        "strategy": "Testing Method",
        column: y_label,
        "method_type": "Method Type",
    },
)

fig.update_traces(
    texttemplate="%{y:.2f}",
    textposition="outside",
)
fig.update_layout(xaxis_tickangle=-15)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Average Results by Method")

display_summary = summary.rename(
    columns={
        "strategy": "Testing Method",
        "method_type": "Method Type",
        "average_bugs": "Average Unique Bugs",
        "average_coverage": "Average Coverage (%)",
        "average_time": "Average Execution Time (seconds)",
        "average_budget": "Average Budget Used",
        "runs": "Runs / Episodes",
    }
)

st.dataframe(
    display_summary.round(4),
    use_container_width=True,
    hide_index=True,
)

if ppo_df is not None:
    st.subheader("PPO Agent Details")

    st.metric(
        "Average PPO Reward",
        f"{ppo_df['total_reward'].mean():.2f}",
    )

    st.caption(
        "PPO reward is reported separately because baseline runs "
        "do not currently calculate reward using the RL environment."
    )

with st.expander("View Raw Experimental Results"):
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

st.caption(
    "Preliminary results on the sample application. PPO is evaluated "
    "over episodes, while baselines repeatedly use a fixed strategy. "
    "Results do not establish that one method is universally better."
)
