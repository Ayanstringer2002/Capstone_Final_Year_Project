import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"
# MODEL_NAME = "llama-3.1-70b-versatile"

def get_financial_advice(user_message, context=""):
    prompt = f"""
You are an expert personal finance advisor.

User context:
{context}

User question:
{user_message}

Give clear, actionable and practical advice in bullet points.
Also suggest how to optimize spending and increase savings.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a smart AI financial advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content
