from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

draft_text = input("Enter your draft text: ")
issue_to_fix = input("Enter the issue to fix: ")

current_draft = draft_text

for round_number in range(1, 4):
    print(f"\n--- Round {round_number} ---")

    system_prompt = """
    You are a content editor.
    Revise the given draft to fix only the specific issue.
    Preserve the original meaning and important information.
    Do not introduce unrelated changes.
    Return only the revised draft.
    """

    user_prompt = f"""
    Original draft:
    {draft_text}

    Current draft:
    {current_draft}

    Specific issue to fix:
    {issue_to_fix}

    This is revision round {round_number} of 3.
    Improve the current draft to address the specific issue.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )

    current_draft = response.choices[0].message.content.strip()
    print(current_draft)

print("\nFinal Revised Draft:")
print(current_draft)