
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


class EMIInput(BaseModel):
    principal: float = Field(gt=0, description="Loan amount")
    annual_rate: float = Field(ge=0, description="Annual interest rate in percent")
    months: int = Field(gt=0, description="Loan duration in months")


def calculate_emi(principal: float, annual_rate: float, months: int) -> str:
    monthly_rate = annual_rate / 12 / 100

    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = principal * monthly_rate * (1 + monthly_rate) ** months
        emi /= (1 + monthly_rate) ** months - 1

    return f"Monthly EMI: ₹{emi:.2f}"


emi_tool = StructuredTool.from_function(
    func=calculate_emi,
    name="calculate_emi",
    description="Calculate the monthly EMI for a loan.",
    args_schema=EMIInput
)

result = emi_tool.invoke({
    "principal": 500000,
    "annual_rate": 8.5,
    "months": 60
})

print(result)
