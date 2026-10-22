from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

system_prompt = """
You are a professional language translator.
Translate the given sentence into the target language.
Follow the requested formality level.
Use formal language for formal requests.
Use casual and friendly language for informal requests.
Preserve the original meaning.
Return only the translated sentence.
"""

sentence = input("Enter sentence: ")
target_language = input("Enter target language: ")
formality = input("Enter formality (formal, neutral, informal): ")

user_prompt = f"""
Sentence: {sentence}
Target language: {target_language}
Formality: {formality}

Translate the sentence according to the requested formality.
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0
)

print("\nTranslated Sentence:")
print(response.choices[0].message.content)