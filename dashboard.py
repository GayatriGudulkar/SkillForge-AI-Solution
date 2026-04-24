import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Learning Agent - Faculty Dashboard", layout="wide")

st.title("🎓 Engineering Learning Analytics Dashboard")
st.markdown("Real-time insights on student struggles and progress")

# Get cohort statistics
response = requests.get(f"{API_URL}/cohort_stats")
stats = response.json() if response.status_code == 200 else {}

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Students", "47")
with col2:
    st.metric("Active Plans", "38")
with col3:
    st.metric("Completion Rate", "68%")

st.subheader("📊 Top Concepts Students Struggle With")

if stats.get("top_struggles"):
    df = pd.DataFrame(stats["top_struggles"])
    fig = px.bar(df, x="topic", y="count", title="Struggle Frequency by Topic")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("📈 Daily Progress Overview")

# Sample progress data
progress_data = pd.DataFrame({
    "Day": list(range(1, 31)),
    "Completion Rate": [45, 52, 58, 62, 68, 72, 75, 78, 80, 82, 84, 85, 86, 87, 88, 89, 90, 91, 91, 92, 92, 93, 93, 94, 94, 95, 95, 96, 96, 97]
})

fig2 = px.line(progress_data, x="Day", y="Completion Rate", title="Average Completion Rate Over Time")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("🎯 Actionable Recommendations for Faculty")

st.info(
    "Based on cohort data:\n\n"
    "• **Week 1-2:** 60% of students struggle with **functions** → Consider in-class demo\n"
    "• **Week 3:** Dictionary comprehension confusion → Add practice worksheet\n"
    "• **Week 4:** Loop optimization → Schedule extra TA hours"
)

st.subheader("👨‍🎓 Student Progress (Sample)")

student_df = pd.DataFrame({
    "Student ID": ["S001", "S002", "S003", "S004", "S005"],
    "Current Day": [12, 8, 15, 5, 20],
    "Completion %": [40, 27, 50, 17, 67],
    "Times Stuck": [3, 5, 2, 7, 1]
})

st.dataframe(student_df, use_container_width=True)