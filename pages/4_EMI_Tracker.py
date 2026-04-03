import streamlit as st
import math
from database.db import add_emi, get_emis, delete_emi
from utils.helpers import convert_emis_to_df
from utils.auth import is_logged_in

st.title("🏦 EMI Tracker")

if not is_logged_in():
    st.warning("Please login first.")
    st.stop()

user = st.session_state.user
user_id = user[0]

st.subheader("➕ Add New EMI Loan")

loan_name = st.text_input("Loan Name (Example: Bike Loan)")
principal = st.number_input("Principal Amount (₹)", min_value=0.0)
interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0)
tenure_months = st.number_input("Tenure (Months)", min_value=1, step=1)
start_date = st.date_input("Loan Start Date")
due_date = st.date_input("Monthly Due Date")

def calculate_emi(P, annual_rate, N):
    r = (annual_rate / 12) / 100
    if r == 0:
        return P / N
    emi = (P * r * ((1 + r) ** N)) / (((1 + r) ** N) - 1)
    return emi

monthly_emi = calculate_emi(principal, interest_rate, tenure_months)

st.info(f"📌 Estimated Monthly EMI: ₹{monthly_emi:.2f}")

if st.button("💾 Save EMI"):
    add_emi(user_id, loan_name, principal, interest_rate, tenure_months,
            str(start_date), str(due_date), monthly_emi)
    st.success("EMI Added Successfully!")

st.subheader("📋 Your EMI Loans")

emis = get_emis(user_id)
df = convert_emis_to_df(emis)

st.dataframe(df, use_container_width=True)

if not df.empty:
    emi_id = st.number_input("Enter EMI ID to delete", min_value=1, step=1)
    if st.button("🗑 Delete EMI"):
        delete_emi(emi_id)
        st.warning("EMI deleted successfully!")
