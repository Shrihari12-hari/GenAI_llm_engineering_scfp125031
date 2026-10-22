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

class FitnessDetails(BaseModel):
    goal_type: str
    fitness_level: str
    days_available: int
    equipment_access: str

class WorkoutDay(BaseModel):
    day: str
    activity: str
    duration_minutes: int
    notes: str

class WeeklyPlan(BaseModel):
    plan: list[WorkoutDay]

parser1 = PydanticOutputParser(pydantic_object=FitnessDetails)

prompt1 = PromptTemplate(
    template="Extract the fitness goal, fitness level, days available per week, and equipment access from this description:\n{goal}\nAvailable days entered by user: {days}\n{format_instructions}",
    input_variables=["goal", "days"],
    partial_variables={"format_instructions": parser1.get_format_instructions()}
)

chain1 = prompt1 | llm | parser1

parser2 = PydanticOutputParser(pydantic_object=WeeklyPlan)

prompt2 = ChatPromptTemplate.from_messages([
    ("system", "You are a certified personal trainer. Create a realistic beginner-safe weekly plan using only the extracted fitness details. Include rest days when appropriate. Avoid unsafe or extreme recommendations."),
    ("human", "Extracted fitness details: {details}\nCreate a plan for the requested number of days per week. Return structured output.\n{format_instructions}")
])

chain2 = prompt2 | llm | parser2

goal = input("Describe your fitness goal: ")
days = input("How many days per week can you exercise? ")

details = chain1.invoke({"goal": goal, "days": days})

print("\nStep 1: Extracted Fitness Details")
print(details.model_dump_json(indent=2))

plan = chain2.invoke({
    "details": details.model_dump_json(),
    "format_instructions": parser2.get_format_instructions()
})

print("\nStep 2: Weekly Workout Plan")
print(plan.model_dump_json(indent=2))