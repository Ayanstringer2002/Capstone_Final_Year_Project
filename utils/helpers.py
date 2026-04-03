import pandas as pd

def convert_expenses_to_df(expenses):
    return pd.DataFrame(expenses, columns=[
        "ID", "UserID", "Date", "Category", "Description", "Type", "Amount"
    ])

def convert_budgets_to_df(budgets):
    return pd.DataFrame(budgets, columns=[
        "ID", "UserID", "Month", "Category", "Budget"
    ])

def convert_emis_to_df(emis):
    return pd.DataFrame(emis, columns=[
        "ID", "UserID", "Loan Name", "Principal", "Interest Rate",
        "Tenure (Months)", "Start Date", "Due Date", "Monthly EMI"
    ])
