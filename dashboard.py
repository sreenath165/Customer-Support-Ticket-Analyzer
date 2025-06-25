import streamlit as st
import pandas as pd
import json
import altair as alt

# Streamlit config
st.set_page_config(
    page_title="Customer Support Ticket Analyzer & Router",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
try:
    with open("results.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    st.error("results.json not found. Please run main.py first.")
    st.stop()

df = pd.DataFrame(data)

# Convert timestamp
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"])

# KPI metrics
st.title("Customer Support Ticket Analyzer & Router")
st.markdown("AI-powered classification of customer tickets by **severity**, **priority**, and **routing logic**.")

col1, col2, col3 = st.columns(3)
col1.metric("Total Tickets", len(df))
col2.metric("Critical Issues", (df["severity_category"] == "critical").sum())
col3.metric("High Priority", (df["priority_level"] == "high").sum())

st.markdown("---")

# Sidebar Filters
st.sidebar.header("Filter Tickets")

# Routing filter
route_options = df["routing_decision"].unique().tolist()
selected_routes = st.sidebar.multiselect("Routing Decisions", route_options, default=route_options)

# Severity filter
severity_options = df["severity_category"].unique().tolist()
selected_severity = st.sidebar.multiselect("Severity Categories", severity_options, default=severity_options)

# Priority filter
priority_options = df["priority_level"].unique().tolist()
selected_priority = st.sidebar.multiselect("Priority Levels", priority_options, default=priority_options)

# Apply filters
filtered_df = df[
    df["routing_decision"].isin(selected_routes) &
    df["severity_category"].isin(selected_severity) &
    df["priority_level"].isin(selected_priority)
]

# Styled table view
st.subheader("Ticket Classification Table")

def highlight_cells(val, col_name):
    if col_name == "severity_score" and val >= 8:
        return "background-color: #ffcccc"  # light red
    elif col_name == "priority_score" and val >= 8:
        return "background-color: #cce5ff"  # light blue
    elif val == "critical":
        return "background-color: #ffb3b3"
    elif val == "high":
        return "background-color: #99ccff"
    return ""

styled_df = filtered_df.style.applymap(lambda v: highlight_cells(v, "severity_score"), subset=["severity_score"])
styled_df = styled_df.applymap(lambda v: highlight_cells(v, "priority_score"), subset=["priority_score"])
styled_df = styled_df.applymap(lambda v: highlight_cells(v, "severity_category"), subset=["severity_category"])
styled_df = styled_df.applymap(lambda v: highlight_cells(v, "priority_level"), subset=["priority_level"])

st.dataframe(styled_df, use_container_width=True)

# Score Distribution Charts
st.subheader("Score Distributions")
col4, col5 = st.columns(2)

with col4:
    st.markdown("**Severity Score Distribution**")
    severity_chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X("severity_score:O", title="Severity Score"),
        y=alt.Y("count():Q", title="Count"),
        tooltip=["severity_score", "count()"]
    ).properties(height=300)
    st.altair_chart(severity_chart, use_container_width=True)

with col5:
    st.markdown("**Priority Score Distribution**")
    priority_chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X("priority_score:O", title="Priority Score"),
        y=alt.Y("count():Q", title="Count"),
        tooltip=["priority_score", "count()"]
    ).properties(height=300)
    st.altair_chart(priority_chart, use_container_width=True)

# Time Trend Charts
if "timestamp" in df.columns:
    st.subheader("Trend Over Time")

    df_sorted = filtered_df.sort_values("timestamp")

    col6, col7 = st.columns(2)

    with col6:
        st.markdown("**Severity Score Over Time**")
        severity_line = alt.Chart(df_sorted).mark_line(point=True).encode(
            x=alt.X("timestamp:T", title="Timestamp"),
            y=alt.Y("severity_score:Q", title="Severity Score"),
            tooltip=["ticket_id", "severity_score"]
        ).properties(height=300)
        st.altair_chart(severity_line, use_container_width=True)

    with col7:
        st.markdown("**Priority Score Over Time**")
        priority_line = alt.Chart(df_sorted).mark_line(point=True).encode(
            x=alt.X("timestamp:T", title="Timestamp"),
            y=alt.Y("priority_score:Q", title="Priority Score"),
            tooltip=["ticket_id", "priority_score"]
        ).properties(height=300)
        st.altair_chart(priority_line, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Customer Support Ticket Analyzer & Router by Y. Sai Sreenath Reddy")
