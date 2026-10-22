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

class Complaint(BaseModel):
    complaint: str = Field(description="Customer complaint")
    product_or_feature: str = Field(description="Product or feature")
    sentiment: str = Field(description="Customer sentiment")

parser = PydanticOutputParser(pydantic_object=Complaint)

prompt1 = PromptTemplate(
    template="Extract complaint, product_or_feature, and sentiment from this review:\n{review}\n{format_instructions}",
    input_variables=["review"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

chain1 = prompt1 | llm | parser

prompt2 = ChatPromptTemplate.from_messages([
    ("system", "You are a support ticket writer. Write a short internal support ticket using only the structured data provided."),
    ("human", "Complaint data: {data}")
])

chain2 = prompt2 | llm | StrOutputParser()

review = input("Enter customer review: ")

data = chain1.invoke({"review": review})
print("\nStep 1: Structured Complaint Data")
print(data.model_dump_json(indent=2))

ticket = chain2.invoke({"data": data.model_dump_json()})
print("\nStep 2: Support Ticket Summary")
print(ticket)