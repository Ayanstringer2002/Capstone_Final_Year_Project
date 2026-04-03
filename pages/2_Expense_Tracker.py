import streamlit as st
from database.db import add_expense, get_expenses, delete_expense
from utils.helpers import convert_expenses_to_df
from utils.auth import is_logged_in

st.title("📌 Daily Expense Tracker")

if not is_logged_in():
    st.warning("Please login first.")
    st.stop()

user = st.session_state.user
user_id = user[0]

date = st.date_input("Date")
category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"])
description = st.text_input("Description")
expense_type = st.selectbox("Expense Type", ["Fixed", "Variable"])
amount = st.number_input("Amount (₹)", min_value=0.0)

if st.button("➕ Add Expense"):
    add_expense(user_id, str(date), category, description, expense_type, amount)
    st.success("Expense added successfully!")

st.subheader("📋 Your Expenses")

expenses = get_expenses(user_id)
df = convert_expenses_to_df(expenses)

st.dataframe(df, use_container_width=True)

if not df.empty:
    expense_id = st.number_input("Expense ID to delete", min_value=1, step=1)
    if st.button("🗑 Delete Expense"):
        delete_expense(expense_id)
        st.warning("Expense deleted!")
