
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

system_prompt = """You are a resume extractor.Extract only the requested fields from the resume.If information is missing, use an empty string.Return only valid JSON. Do not add explanations.
"""

resume_text = input("Enter resume text: ")
fields = input("Enter fields to extract: ")

user_prompt = f"""
Resume: {resume_text}
Extract these fields: {fields}
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0
)

print(response.choices[0].message.content)
