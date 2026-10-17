import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Add Entry")

entry_type = st.selectbox("Type", ["spent", "won"])
entry_date = st.date_input("Date")
entry_amount = st.number_input("Amount (€)", min_value=0.0, step=0.5)

if st.button("Add Entry"):
    payload = {
        "date": entry_date.isoformat(),
        "type": entry_type,
        "amount": entry_amount
    }
    r = requests.post(f"{API_URL}/entries/", json=payload)
    if r.status_code == 200:
        st.success("Entry added successfully.")
    else:
        st.error("Failed to add entry.")
