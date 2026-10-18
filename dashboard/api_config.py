import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

API_URL = "http://localhost:8000"

try:
    if "API_URL" in st.secrets:
        API_URL = st.secrets["API_URL"]
except (StreamlitSecretNotFoundError, FileNotFoundError):
    pass
