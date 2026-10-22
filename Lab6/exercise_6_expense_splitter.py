
from langchain_core.tools import tool


@tool
def split_expense(total_amount: float, number_of_people: int) -> str:
    """Split a total expense equally among a group of people."""
    if total_amount < 0:
        return "Error: Amount cannot be negative."

    if number_of_people <= 0:
        return "Error: Number of people must be greater than zero."

    share = total_amount / number_of_people

    return (
        f"Total expense: ₹{total_amount:.2f}\n"
        f"Number of people: {number_of_people}\n"
        f"Each person pays: ₹{share:.2f}"
    )


result = split_expense.invoke({
    "total_amount": 1500,
    "number_of_people": 5
})

print(result)
