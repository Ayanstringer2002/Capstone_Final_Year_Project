def generate_spending_alerts(df_exp, salary):
    alerts = []

    if df_exp.empty:
        return alerts

    category_spend = df_exp.groupby("Category")["Amount"].sum()

    for category, spent in category_spend.items():
        percent = (spent / salary) * 100 if salary > 0 else 0

        if percent >= 40:
            alerts.append(f"⚠️ Your spending on {category} is {percent:.1f}% of salary. Reduce it.")
        elif percent >= 25:
            alerts.append(f"🔔 Your spending on {category} is {percent:.1f}% of salary. Monitor carefully.")

    return alerts
