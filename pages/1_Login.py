import streamlit as st
from database.db import register_user, login_user

st.title("🔐 Login / Register")

menu = st.radio("Choose Option", ["Login", "Register"])

if menu == "Register":
    st.subheader("Create New Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    salary = st.number_input("Monthly Salary (₹)", min_value=0.0)
    savings_goal = st.number_input("Monthly Savings Goal (₹)", min_value=0.0)

    if st.button("Register"):
        try:
            register_user(username, password, salary, savings_goal)
            st.success("Account created successfully. Now login!")
        except:
            st.error("Username already exists!")

if menu == "Login":
    st.subheader("Login Here")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.user = user
            st.success(f"Welcome {user[1]} 🎉")
        else:
            st.error("Invalid username/password")
