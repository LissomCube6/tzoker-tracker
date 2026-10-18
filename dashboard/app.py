import streamlit as st
from pathlib import Path

# let's fix the paths starting from the root of the project
project_root = Path(__file__).parent

# Navigation
pages = [
    st.Page(str(project_root / "pages" / "1_Dashboard.py"), title="Dashboard"),
    st.Page(str(project_root / "pages" / "2_History.py"), title="History"),
    st.Page(str(project_root / "pages" / "3_Analytics.py"), title="Analytics"),
    st.Page(str(project_root / "pages" / "4_Add_Entry.py"), title="Add Entries"),
    st.Page(str(project_root / "pages" / "5_Add_Repayment.py"),
            title="Repayments"),
]

pg = st.navigation(pages, position="sidebar")
pg.run()
