
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
import os

# Load the .env file from the same folder as this Python script
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Read the API key securely
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Check that your .env file "
        "exists in the same folder as this Python script."
    )

# Initialize Groq client
client = Groq(api_key=api_key)

# System prompt

system_prompt = """
You are a medical note summarization assistant.

Generate these sections:
1. Symptoms
2. Diagnosis
3. Recommendations
4. Missing Information

Rules:
- Use only information supported by the patient notes.
- Never invent symptoms, diagnoses, medical history, or treatments.
- If symptoms are not mentioned, state:
  "No symptoms explicitly reported."
- If the input is meaningless, random characters, or
  unrelated to medical information, state:
  "Invalid or insufficient medical information provided."
- If the notes are invalid or meaningless, do not generate
  generic medical recommendations. Ask the user to enter
  valid patient notes instead.
- If diagnosis is absent, state "Not provided."
- Recommendations must be relevant to the reported information.
- Use plain text headings and bullet points.
- Do not use Markdown tables or HTML tags.
"""
# User prompt
user_prompt = (
    "Create a structured medical summary from the "
    "patient's details below."
)

# Get patient information
name = input("Enter patient name: ").strip()
notes = input("Enter patient notes: ").strip()

if not name or not notes:
    raise ValueError("Patient name and notes cannot be empty.")

# Create user message
user_message = f"""
{user_prompt}

Patient Name: {name}
Patient Notes: {notes}
"""

try:
    # Send request to Groq
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.2
    )

    # Display result
    summary = response.choices[0].message.content

    print("\n" + "=" * 45)
    print("          DOCTOR SUMMARY")
    print("=" * 45)
    print(f"Patient Name: {name}")
    print("-" * 45)
    print(summary)
    print("=" * 45)

except Exception as e:
    print(f"\nError generating summary: {e}")
