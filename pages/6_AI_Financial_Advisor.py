import streamlit as st
from database.db import get_expenses, get_budgets, get_emis
from utils.helpers import convert_expenses_to_df, convert_budgets_to_df, convert_emis_to_df
from utils.groq_ai import get_financial_advice
from utils.auth import is_logged_in

st.title("🤖 AI Financial Advisor (Groq)")

if not is_logged_in():
    st.warning("Please login first.")
    st.stop()

user = st.session_state.user
user_id = user[0]
username = user[1]
salary = user[3]
savings_goal = user[4]

expenses = get_expenses(user_id)
budgets = get_budgets(user_id)
emis = get_emis(user_id)

df_exp = convert_expenses_to_df(expenses)
df_budget = convert_budgets_to_df(budgets)
df_emi = convert_emis_to_df(emis)

context = f"""
User: {username}
Salary: {salary}
Savings Goal: {savings_goal}
"""

if not df_exp.empty:
    context += "\nTotal Expenses: " + str(df_exp["Amount"].sum())
    context += "\nCategory Wise Spending:\n"
    context += df_exp.groupby("Category")["Amount"].sum().to_string()

if not df_budget.empty:
    context += "\n\nBudgets:\n"
    context += df_budget.groupby("Category")["Budget"].sum().to_string()

if not df_emi.empty:
    context += "\n\nEMI Details:\n"
    context += df_emi[["Loan Name", "Monthly EMI", "Due Date"]].to_string(index=False)

st.subheader("💬 Chat with AI Financial Advisor")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask: How can I save more? Should I close my EMI?")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    ai_reply = get_financial_advice(user_input, context)

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    with st.chat_message("assistant"):
        st.markdown(ai_reply)
