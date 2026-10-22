from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import os

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

class Answer(BaseModel):
    question: str
    answer: str

class Answers(BaseModel):
    answers: list[Answer]

class SkillResult(BaseModel):
    skill: str
    demonstrated: bool
    evidence_or_gap: str

class SkillResults(BaseModel):
    results: list[SkillResult]

class ScorecardRow(BaseModel):
    skill: str
    demonstrated: bool
    evidence_or_gap: str

class Scorecard(BaseModel):
    rows: list[ScorecardRow]
    overall_recommendation: str

parser1 = PydanticOutputParser(pydantic_object=Answers)
parser2 = PydanticOutputParser(pydantic_object=SkillResults)
parser3 = PydanticOutputParser(pydantic_object=Scorecard)

prompt1 = PromptTemplate(
    template="Extract every interview question and the candidate's answer from this transcript. Do not invent missing answers.\nTranscript: {transcript}\n{format_instructions}",
    input_variables=["transcript"],
    partial_variables={"format_instructions": parser1.get_format_instructions()}
)

chain1 = prompt1 | llm | parser1

prompt2 = ChatPromptTemplate.from_messages([
    ("system", "You are a technical interviewer evaluating skill evidence. Mark a skill demonstrated only when the answers clearly support it. Otherwise, set demonstrated to false and explain the gap."),
    ("human", "Extracted answers:\n{answers}\nSkills to assess:\n{skills}\n{format_instructions}")
])

chain2 = prompt2 | llm | parser2

prompt3 = ChatPromptTemplate.from_messages([
    ("system", "You are a hiring panel coordinator. Prepare a clear scorecard based only on the supplied skill evaluation. Do not invent evidence. Give a cautious overall recommendation."),
    ("human", "Skill evaluation:\n{evaluation}\n{format_instructions}")
])

chain3 = prompt3 | llm | parser3

transcript_text = input("Enter interview transcript: ")
skills_to_assess = input("Enter skills to assess, separated by commas: ")

answers = chain1.invoke({"transcript": transcript_text})

print("\nStep 1: Extracted Answers")
print(answers.model_dump_json(indent=2))

evaluation = chain2.invoke({
    "answers": answers.model_dump_json(),
    "skills": skills_to_assess,
    "format_instructions": parser2.get_format_instructions()
})

print("\nStep 2: Skill Evaluation")
print(evaluation.model_dump_json(indent=2))

scorecard = chain3.invoke({
    "evaluation": evaluation.model_dump_json(),
    "format_instructions": parser3.get_format_instructions()
})

print("\nStep 3: Final Hiring Scorecard")
print(scorecard.model_dump_json(indent=2))