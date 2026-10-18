import os

import streamlit as st
from dotenv import load_dotenv
from streamlit.errors import StreamlitSecretNotFoundError

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")

try:
    if "API_URL" in st.secrets:
        API_URL = st.secrets["API_URL"]
except (StreamlitSecretNotFoundError, FileNotFoundError):
    pass
