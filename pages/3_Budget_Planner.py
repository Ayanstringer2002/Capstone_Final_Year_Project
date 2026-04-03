import streamlit as st
import pandas as pd
from database.db import add_budget, get_budgets, get_expenses
from utils.helpers import convert_budgets_to_df, convert_expenses_to_df
from utils.auth import is_logged_in
from utils.ai_budget import generate_ai_budget

st.title("📊 Budget Planner + AI Auto Budget")

if not is_logged_in():
    st.warning("Please login first.")
    st.stop()

user = st.session_state.user
user_id = user[0]
salary = user[3]
savings_goal = user[4]

st.info(f"💰 Salary: ₹{salary} | 🎯 Savings Goal: ₹{savings_goal}")

# ---------------- Manual Budget Entry ---------------- #
st.subheader("📝 Manual Budget Entry")

month = st.text_input("Month (Example: 2026-02)")
category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"])
budget_amount = st.number_input("Budget Amount (₹)", min_value=0.0)

if st.button("💾 Save Budget"):
    add_budget(user_id, month, category, budget_amount)
    st.success("Budget saved successfully!")

# ---------------- AI Auto Budget Generator ---------------- #
st.subheader("🤖 AI Monthly Budget Auto Generation")

if st.button("⚡ Generate AI Budget Plan"):
    expenses = get_expenses(user_id)
    df_exp = convert_expenses_to_df(expenses)

    if df_exp.empty:
        st.warning("Not enough expense data. Add some expenses first.")
    else:
        summary = df_exp.groupby("Category")["Amount"].sum().to_string()

        ai_budget = generate_ai_budget(salary, savings_goal, summary)

        if ai_budget is None:
            st.error("AI could not generate valid JSON budget. Try again.")
        else:
            st.success("AI Budget Plan Generated Successfully!")

            ai_df = pd.DataFrame(ai_budget.items(), columns=["Category", "Suggested Budget"])
            st.dataframe(ai_df, use_container_width=True)

            if month.strip() == "":
                st.warning("Enter month above before saving AI budget.")
            else:
                if st.button("✅ Save AI Budget to Database"):
                    for cat, amt in ai_budget.items():
                        add_budget(user_id, month, cat, float(amt))
                    st.success("AI Budget saved successfully!")

# ---------------- Budget Records ---------------- #
st.subheader("📌 Your Budget Records")

budgets = get_budgets(user_id)
df_budget = convert_budgets_to_df(budgets)

st.dataframe(df_budget, use_container_width=True)

