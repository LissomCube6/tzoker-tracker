import streamlit as st
import pandas as pd
import requests
from api_config import API_URL

st.title("Amount Owed and Repayments")

# Add filters for date range
col1, col2 = st.columns(2)
start_date = col1.date_input("Start Date", value=None, format="DD/MM/YYYY")
end_date = col2.date_input("End Date", value=None, format="DD/MM/YYYY")

params = {}  # Filter for spent entries only
if start_date:
    params["start_date"] = start_date.isoformat()
if end_date:
    params["end_date"] = end_date.isoformat()
# params["type"] = "spent"  # Only fetch spent entries for calculating owed amount


# Fetch entries and repayments using the filter dates
r_entries = requests.get(f"{API_URL}/entries/",
                         params=params.update({"type": "spent"}))
r_repayments = requests.get(f"{API_URL}/repayments/", params=params)

# Convert responses to DataFrames
df_entries = pd.DataFrame(r_entries.json())
df_repayments = pd.DataFrame(r_repayments.json())

# Calculate total spent and total repayments
total_spent = df_entries[df_entries["type"] == "spent"]["amount"].sum()
total_repaid = df_repayments["amount"].sum() if not df_repayments.empty else 0

# Calculate amount owed
amount_owed = total_spent - total_repaid

# Display owed amount
st.subheader("Current Balance")
if amount_owed < 0:
    st.success(
        f"You have overpaid! Amount to be refunded: €{-amount_owed:.2f}")
else:
    st.metric("Amount Owed", f"€{amount_owed:.2f}")

# st.divider()

st.subheader("Add Repayment")

with st.form(key="repayment_form", clear_on_submit=True):

    col1, col2 = st.columns(2)
    repayment_date = col1.date_input("Repayment Date")
    repayment_amount = col2.number_input(
        "Repayment Amount (€)", min_value=0.0, step=0.5)

    colA, colB = st.columns([0.25, 1], gap='xxsmall')
    submitted = colA.form_submit_button("Add Repayment")
    submitted_full = colB.form_submit_button("Repay Full Amount")

    # submitted = st.form_submit_button("Add Repayment")
    if submitted:
        if repayment_amount <= 0:
            st.error("Repayment amount must be greater than zero.")
        else:
            repayment_data = {
                "date": repayment_date.isoformat(),
                "amount": repayment_amount
            }
            response = requests.post(
                f"{API_URL}/repayments/", json=repayment_data)
            if response.status_code == 200:
                st.success("Repayment added successfully!")
                st.rerun()  # Refresh the page to update the owed amount
            else:
                st.error("Failed to add repayment. Please try again.")

    if submitted_full:
        if amount_owed <= 0:
            st.info("No amount owed to repay.")
        else:
            full_repayment_data = {
                "date": pd.Timestamp.now().date().isoformat(),
                "amount": amount_owed
            }
            response = requests.post(
                f"{API_URL}/repayments/", json=full_repayment_data)
            if response.status_code == 200:
                st.success("Full repayment added successfully!")
                st.rerun()  # Refresh the page to update the owed amount
            else:
                st.error("Failed to add full repayment. Please try again.")

# st.divider()

# # Repayment log
# st.subheader("Repayment Log")

# if df_repayments.empty:
#     st.info("No repayments recorded yet.")

# else:
#     # Toggle state
#     if "show_all_repayments" not in st.session_state:
#         st.session_state.show_all_repayments = False

#     # Button logic
#     if st.session_state.show_all_repayments:
#         st.write("All Repayments:")
#         st.dataframe(df_repayments[["date", "amount"]].sort_values("date", ascending=False))
#         if st.button("Show last 10 repayments"):
#             st.session_state.show_all_repayments = False
#             # st.rerun()
#     else:
#         st.write("Last 10 Repayments:")
#         last_10_repayments = df_repayments.tail(10)
#         st.dataframe(last_10_repayments[["date", "amount"]].sort_values("date", ascending=False))
#         if st.button("Show all repayments"):
#             st.session_state.show_all_repayments = True
#             # st.rerun()

# --- Repayment Log ---
st.subheader("Repayment Log")

if df_repayments.empty:
    st.info("No repayments recorded yet.")
else:
    # Initialize toggle state
    if "show_all_repayments" not in st.session_state:
        st.session_state.show_all_repayments = False

    # Determine which table to show
    if st.session_state.show_all_repayments:
        st.write("Showing all repayments:")
        st.dataframe(df_repayments)

        # Collapse button
        if st.button("Show last 10 repayments"):
            st.session_state.show_all_repayments = False

    else:
        st.write("Showing last 10 repayments:")
        st.dataframe(df_repayments.tail(10))

        # Expand button
        if st.button("Show all repayments"):
            st.session_state.show_all_repayments = True
