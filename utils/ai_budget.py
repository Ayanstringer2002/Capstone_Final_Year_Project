import json
import re
from utils.groq_ai import client

MODEL_NAME = "llama-3.1-8b-instant"

CATEGORIES = [
    "Food", "Transport", "Shopping",
    "Bills", "Entertainment", "Health", "Other"
]

def extract_json(text):
    """Extract JSON safely from LLM output"""
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception as e:
        print("JSON extraction error:", e)
    return None


def validate_percentages(data):
    """Ensure all categories exist & total = 100"""
    if not data:
        return False

    total = sum(data.values())

    if set(data.keys()) != set(CATEGORIES):
        return False

    if not (95 <= total <= 105):  # Allow small variation
        return False

    return True


def fallback_percentages():
    """Safe default allocation"""
    return {
        "Food": 20,
        "Transport": 10,
        "Shopping": 10,
        "Bills": 30,
        "Entertainment": 10,
        "Health": 10,
        "Other": 10
    }


def convert_to_amounts(percentages, salary, savings_goal):
    """Convert % → ₹ amounts"""
    usable_income = salary - savings_goal
    budget = {}

    for category, percent in percentages.items():
        budget[category] = round((percent / 100) * usable_income)

    return budget


def generate_ai_budget(salary, savings_goal, expense_summary):
    prompt = f"""
You are a financial planning AI.

STRICT RULES:
- Return ONLY JSON
- No explanation, no markdown
- Values must be percentages
- Total must equal 100

User salary: {salary}
Savings goal: {savings_goal}

Past spending:
{expense_summary}

Output format:
{{
  "Food": number,
  "Transport": number,
  "Shopping": number,
  "Bills": number,
  "Entertainment": number,
  "Health": number,
  "Other": number
}}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        ai_text = response.choices[0].message.content.strip()

        print("\n🔍 RAW AI RESPONSE:\n", ai_text)

        percentages = extract_json(ai_text)

        if not validate_percentages(percentages):
            print("⚠️ Invalid AI output, using fallback...")
            percentages = fallback_percentages()

    except Exception as e:
        print("❌ AI ERROR:", e)
        percentages = fallback_percentages()

    # Convert to actual ₹ amounts
    return convert_to_amounts(percentages, salary, savings_goal)