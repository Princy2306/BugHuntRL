
import pandas as pd
import plotly.express as px


# Load the evaluation results.
df = pd.read_csv("strategy_results.csv")

# Calculate average metrics for each strategy.
summary = (
    df.groupby("strategy", as_index=False)
    .agg(
        average_bugs=("unique_bugs_found", "mean"),
        average_coverage=("coverage_percent", "mean"),
        average_time=("execution_time_seconds", "mean"),
        execution_cost=("execution_cost", "mean"),
    )
)

# Graph 1: Average unique bugs found.
fig_bugs = px.bar(
    summary,
    x="strategy",
    y="average_bugs",
    title="Average Unique Bugs Found by Strategy",
    labels={
        "strategy": "Testing Strategy",
        "average_bugs": "Average Unique Bugs",
    },
    text_auto=".2f",
)
fig_bugs.write_html("bugs_comparison.html")

# Graph 2: Average code coverage.
fig_coverage = px.bar(
    summary,
    x="strategy",
    y="average_coverage",
    title="Average Statement Coverage by Strategy",
    labels={
        "strategy": "Testing Strategy",
        "average_coverage": "Coverage (%)",
    },
    text_auto=".2f",
)
fig_coverage.update_yaxes(range=[0, 100])
fig_coverage.write_html("coverage_comparison.html")

# Graph 3: Average execution time.
fig_time = px.bar(
    summary,
    x="strategy",
    y="average_time",
    title="Average Execution Time by Strategy",
    labels={
        "strategy": "Testing Strategy",
        "average_time": "Execution Time (seconds)",
    },
    text_auto=".4f",
)
fig_time.write_html("execution_time_comparison.html")

# Print the summary for verification.
print("\nStrategy comparison:")
print(summary.round(3).to_string(index=False))

print("\nCreated graphs:")
print("- bugs_comparison.html")
print("- coverage_comparison.html")
print("- execution_time_comparison.html")
