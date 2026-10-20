import streamlit as st
import pandas as pd
import requests
from api_config import API_URL

st.title("History")

# Filters
col1, col2, col3 = st.columns(3)
start = col1.date_input("Start date", value=None, format="DD/MM/YYYY")
end = col2.date_input("End date", value=None, format="DD/MM/YYYY")
type_filter = col3.selectbox("Type", ["Both", "spent", "won"])

params = {}
if start:
    params["start_date"] = start.isoformat()
if end:
    params["end_date"] = end.isoformat()
if type_filter != "Both":
    params["type"] = type_filter

r = requests.get(f"{API_URL}/entries/", params=params)
df = pd.DataFrame(r.json())

if df.empty:
    st.info("No entries found.")
    st.stop()

df["date"] = pd.to_datetime(df["date"])

# Summary
spent = df[df["type"] == "spent"]["amount"].sum()
won = df[df["type"] == "won"]["amount"].sum()
net = won - spent

c1, c2, c3 = st.columns(3)
c1.metric("Total Spent", f"€{spent:.2f}")
c2.metric("Total Won", f"€{won:.2f}")
c3.metric("Net", f"€{net:.2f}")

# Table
st.subheader("History Log")
st.dataframe(
    df.sort_values("date"),
    column_config={"date": st.column_config.DateColumn(format="DD/MM/YYYY")},
)
