import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:8000"

st.title("Dashboard")

# Filters
col1, col2 = st.columns(2)
start = col1.date_input("Start date", value=None)
end = col2.date_input("End date", value=None)

params = {}
if start:
    params["start_date"] = start.isoformat()
if end:
    params["end_date"] = end.isoformat()

r = requests.get(f"{API_URL}/entries/", params=params)
df = pd.DataFrame(r.json())

if df.empty:
    st.info("No entries found for selected period.")
    st.stop()

# Summary
spent = df[df["type"]=="spent"]["amount"].sum()
won = df[df["type"]=="won"]["amount"].sum()
net = won - spent

c1, c2, c3 = st.columns(3)
c1.metric("Total Spent", f"€{spent:.2f}")
c2.metric("Total Won", f"€{won:.2f}")
c3.metric("Net", f"€{net:.2f}")

# Charts
st.subheader("Spend vs Win")
df_chart = df.groupby(["date","type"])["amount"].sum().unstack(fill_value=0)
st.bar_chart(df_chart)

st.subheader("Net Over Time")
df_net = df_chart.copy()
df_net["net"] = df_net.get("won", 0) - df_net.get("spent", 0)
st.line_chart(df_net["net"])

# Recent entries
st.subheader("Recent Entries")
st.dataframe(df[["date", "type", "amount"]].sort_values("date").tail(10))
