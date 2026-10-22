from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
import os

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

class SupportSummary(BaseModel):
    issue: str
    customer_tone: str
    resolution_attempted: str

class EscalationCheck(BaseModel):
    missing_fields: list[str]
    is_ready_to_escalate: bool

parser1 = PydanticOutputParser(pydantic_object=SupportSummary)

prompt1 = PromptTemplate(
    template="Extract the issue, customer tone, and attempted resolution from this support chat. Use 'Not provided' for missing details.\nChat: {chat}\n{format_instructions}",
    input_variables=["chat"],
    partial_variables={"format_instructions": parser1.get_format_instructions()}
)

chain1 = prompt1 | llm | parser1

parser2 = PydanticOutputParser(pydantic_object=EscalationCheck)

prompt2 = ChatPromptTemplate.from_messages([
    ("system", "You are an escalation-readiness reviewer. Check whether the support summary contains an issue, account ID, error code, and resolution attempted. List missing information. Mark ready only when the required information is available."),
    ("human", "Support summary: {summary}\n{format_instructions}")
])

chain2 = prompt2 | llm | parser2

prompt3 = ChatPromptTemplate.from_messages([
    ("system", "You are a support operations lead. Write a prioritized escalation report based only on the summary and gap check. Do not invent missing details."),
    ("human", "Summary: {summary}\nGap check: {check}\nWrite the escalation report.")
])

chain3 = prompt3 | llm | StrOutputParser()

chat = input("Enter support chat log: ")

summary = chain1.invoke({"chat": chat})

print("\nStep 1: Structured Summary")
print(summary.model_dump_json(indent=2))

check = chain2.invoke({
    "summary": summary.model_dump_json(),
    "format_instructions": parser2.get_format_instructions()
})

print("\nStep 2: Missing Information Check")
print(check.model_dump_json(indent=2))

report = chain3.invoke({
    "summary": summary.model_dump_json(),
    "check": check.model_dump_json()
})

print("\nStep 3: Escalation Report")
print(report)