
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
import os

load_dotenv()

@tool
def get_order_status(order_id: str) -> str:
    """Look up the shipping status of an order using its order ID."""
    orders = {
        "ORD-4521": "Shipped and arriving tomorrow",
        "ORD-4522": "Processing",
        "ORD-4523": "Delivered"
    }
    return orders.get(order_id, "Order ID not found")

model = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

model_with_tools = model.bind_tools([get_order_status])

user_query = input("Ask about your order: ")

messages = [{"role": "user", "content": user_query}]
response = model_with_tools.invoke(messages)

print("\nSuggested tool calls:")
print(response.tool_calls)

for call in response.tool_calls:
    if call["name"] == "get_order_status":
        result = get_order_status.invoke(call["args"])
        print("\nTool result:", result)
        messages.append(response)
        messages.append({
            "role": "tool",
            "tool_call_id": call["id"],
            "content": result
        })

final_response = model.invoke(messages)
print("\nFinal answer:")
print(final_response.content)
