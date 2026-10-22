from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

system_prompt = """
You are a customer support assistant.
Write a polite, friendly, and professional reply.
Keep the tone consistent for every customer.
Use simple language.
Do not exceed the given word limit.
Return only the customer support reply.
"""

customer_message = input("Enter customer message: ")
company_name = input("Enter company name: ")
max_words = int(input("Enter maximum word limit: "))

user_prompt = f"""
Company name: {company_name}
Customer message: {customer_message}
Maximum words: {max_words}

Write a helpful customer support reply.
Stay within the word limit.
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0
)

print("\nCustomer Support Reply:")
print(response.choices[0].message.content)