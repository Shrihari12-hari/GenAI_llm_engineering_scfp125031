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

class ResearchData(BaseModel):
    research_question: str = Field(description="Research question")
    method: str = Field(description="Research method")
    key_finding: str = Field(description="Main finding")

parser = PydanticOutputParser(pydantic_object=ResearchData)

prompt1 = PromptTemplate(
    template="Extract the research question, method, and key finding from this abstract:\n{abstract}\n{format_instructions}",
    input_variables=["abstract"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

chain1 = prompt1 | llm | parser

prompt2 = ChatPromptTemplate.from_messages([
    ("system", "You are a science communicator explaining research to a general audience. Use simple language."),
    ("human", "Research data: {data}\nWrite a short, easy-to-understand summary using only this data.")
])

chain2 = prompt2 | llm | StrOutputParser()

abstract = input("Enter research paper abstract: ")

data = chain1.invoke({"abstract": abstract})

print("\nStep 1: Structured Research Data")
print(data.model_dump_json(indent=2))

summary = chain2.invoke({"data": data.model_dump_json()})

print("\nStep 2: Layperson Summary")
print(summary)