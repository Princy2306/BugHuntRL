
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
    "Compare testing strategies using bug detection, "
    "code coverage, and execution time."
)

RESULTS_FILE = "strategy_results.csv"

try:
    df = pd.read_csv(RESULTS_FILE)
except FileNotFoundError:
    st.error(
        f"{RESULTS_FILE} not found. "
        "Run evaluate_testing_strategies.py first."
    )
    st.stop()

required_columns = {
    "strategy",
    "run",
    "unique_bugs_found",
    "coverage_percent",
    "execution_time_seconds",
    "execution_cost",
}

missing_columns = required_columns - set(df.columns)

if missing_columns:
    st.error(f"Missing CSV columns: {', '.join(sorted(missing_columns))}")
    st.stop()

summary = (
    df.groupby("strategy", as_index=False)
    .agg(
        average_bugs=("unique_bugs_found", "mean"),
        average_coverage=("coverage_percent", "mean"),
        average_time=("execution_time_seconds", "mean"),
        average_cost=("execution_cost", "mean"),
    )
)

st.subheader("Experiment Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Testing Strategies", df["strategy"].nunique())
col2.metric("Total Experimental Runs", len(df))
col3.metric("Average Unique Bugs", f"{df['unique_bugs_found'].mean():.2f}")

st.divider()

st.subheader("Strategy Comparison")

metric = st.selectbox(
    "Choose a metric",
    [
        "Average Unique Bugs",
        "Average Code Coverage (%)",
        "Average Execution Time (seconds)",
        "Average Execution Cost",
    ],
)

metric_columns = {
    "Average Unique Bugs": ("average_bugs", "Average unique bugs found"),
    "Average Code Coverage (%)": ("average_coverage", "Coverage (%)"),
    "Average Execution Time (seconds)": (
        "average_time",
        "Execution time (seconds)",
    ),
    "Average Execution Cost": ("average_cost", "Configured strategy cost"),
}

column, y_label = metric_columns[metric]

fig = px.bar(
    summary,
    x="strategy",
    y=column,
    color="strategy",
    text=column,
    title=metric,
    labels={"strategy": "Testing Strategy", column: y_label},
)

fig.update_traces(texttemplate="%{y:.2f}", textposition="outside")
fig.update_layout(showlegend=False, xaxis_tickangle=-15)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Average Results by Strategy")

display_summary = summary.rename(
    columns={
        "strategy": "Testing Strategy",
        "average_bugs": "Average Unique Bugs",
        "average_coverage": "Average Coverage (%)",
        "average_time": "Average Execution Time (seconds)",
        "average_cost": "Average Configured Cost",
    }
)

st.dataframe(
    display_summary.round(4),
    use_container_width=True,
    hide_index=True,
)

with st.expander("View Raw Experimental Results"):
    st.dataframe(df, use_container_width=True, hide_index=True)

st.caption(
    "These are preliminary results from the sample application. "
    "They do not establish that one strategy is universally better."
)
