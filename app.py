import streamlit as st
from database.db import create_tables

st.set_page_config(page_title="AI Finance Tracker", layout="wide")
create_tables()

st.title("💰 AI Finance Tracker (Multi User + EMI + AI Alerts)")
st.sidebar.success("Choose a page from sidebar 🚀")
