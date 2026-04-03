import streamlit as st

def is_logged_in():
    return "user" in st.session_state and st.session_state.user is not None

def logout():
    st.session_state.user = None
