from dotenv import load_dotenv
from groq import Groq
import os
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
system_prompt="""You are a customer review classifier.Classify the review into one category:Positive, Negative, Suggestion, or Neutral.

Positive: Customer is satisfied.
Negative: Customer is dissatisfied.
Suggestion: Customer recommends an improvement.
Neutral: Review is factual without clear sentiment.

Return only one category label"""

review_text = input("Enter customer review: ")
user_message = f"Classify this review: {review_text}"

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ],
    temperature=0
)

print("Category:", response.choices[0].message.content.strip())
