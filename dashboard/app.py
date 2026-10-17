import streamlit as st

# Navigation
pages = [
        st.Page(r"pages\1_Dashboard.py", title="Dashboard"),
        st.Page(r"pages\2_History.py", title="History"),
        st.Page(r"pages\3_Analytics.py", title="Analytics"),
        st.Page(r"pages\4_Add_Entry.py", title="Add Entries"),
        st.Page(r"pages\5_Add_Repayment.py", title="Add Repayments"),
    ]

pg = st.navigation(pages, position="sidebar")
pg.run()