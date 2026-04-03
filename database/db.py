import sqlite3

DB_NAME = "database/finance.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            salary REAL,
            savings_goal REAL
        )
    """)

    # EXPENSES TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            category TEXT,
            description TEXT,
            expense_type TEXT,
            amount REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # BUDGET TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            month TEXT,
            category TEXT,
            budget_amount REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # EMI TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            loan_name TEXT,
            principal REAL,
            interest_rate REAL,
            tenure_months INTEGER,
            start_date TEXT,
            due_date TEXT,
            monthly_emi REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# ---------------- USER FUNCTIONS ---------------- #

def register_user(username, password, salary, savings_goal):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, password, salary, savings_goal)
        VALUES (?, ?, ?, ?)
    """, (username, password, salary, savings_goal))

    conn.commit()
    conn.close()

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users WHERE username=? AND password=?
    """, (username, password))

    user = cursor.fetchone()
    conn.close()
    return user


# ---------------- EXPENSE FUNCTIONS ---------------- #

def add_expense(user_id, date, category, description, expense_type, amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (user_id, date, category, description, expense_type, amount)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, date, category, description, expense_type, amount))

    conn.commit()
    conn.close()

def get_expenses(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM expenses WHERE user_id=?
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()


# ---------------- BUDGET FUNCTIONS ---------------- #

def add_budget(user_id, month, category, budget_amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO budgets (user_id, month, category, budget_amount)
        VALUES (?, ?, ?, ?)
    """, (user_id, month, category, budget_amount))

    conn.commit()
    conn.close()

def get_budgets(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM budgets WHERE user_id=?
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows


# ---------------- EMI FUNCTIONS ---------------- #

def add_emi(user_id, loan_name, principal, interest_rate, tenure_months, start_date, due_date, monthly_emi):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO emis (user_id, loan_name, principal, interest_rate, tenure_months, start_date, due_date, monthly_emi)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, loan_name, principal, interest_rate, tenure_months, start_date, due_date, monthly_emi))

    conn.commit()
    conn.close()

def get_emis(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM emis WHERE user_id=?
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_emi(emi_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM emis WHERE id=?", (emi_id,))
    conn.commit()
    conn.close()
