import streamlit as st
import pandas as pd
import requests
from api_config import API_URL

st.title("Analytics")

r = requests.get(f"{API_URL}/entries/")
df = pd.DataFrame(r.json())

if df.empty:
    st.info("No data available.")
    st.stop()

df["date"] = pd.to_datetime(df["date"])

# Key stats
avg_spent = df[df["type"] == "spent"]["amount"].mean()
avg_won = df[df["type"] == "won"]["amount"].mean()
ratio = (df[df["type"] == "won"]["amount"].sum() /
         df[df["type"] == "spent"]["amount"].sum()) * 100

best_day = df.groupby("date").apply(
    lambda x: x[x["type"] == "won"]["amount"].sum() -
    x[x["type"] == "spent"]["amount"].sum()
).idxmax()

best_value = df.groupby("date").apply(
    lambda x: x[x["type"] == "won"]["amount"].sum() -
    x[x["type"] == "spent"]["amount"].sum()
).max()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Avg Spend", f"€{avg_spent:.2f}")
c2.metric("Avg Win", f"€{avg_won:.2f}")
c3.metric("Win/Spend Ratio", f"{ratio:.2f}%")
c4.metric("Best Day", f"{best_value:.2f}€", f"{best_day:%d/%m/%Y}")

# Charts
st.subheader("Cumulative Net")
df_chart = df.groupby(["date", "type"])["amount"].sum().unstack(fill_value=0)
df_chart["net"] = df_chart.get("won", 0) - df_chart.get("spent", 0)
df_chart["cumulative"] = df_chart["net"].cumsum()
st.line_chart(df_chart["cumulative"])

st.subheader("Spend Distribution")
st.bar_chart(df[df["type"] == "spent"]["amount"])

st.subheader("Win Distribution")
st.bar_chart(df[df["type"] == "won"]["amount"])
