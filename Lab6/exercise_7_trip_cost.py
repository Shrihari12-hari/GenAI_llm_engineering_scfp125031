
from langchain_core.tools import tool


@tool
def calculate_travel_cost(distance_km: float, cost_per_km: float) -> str:
    """Calculate the total travel cost."""
    return f"{distance_km * cost_per_km:.2f}"


@tool
def calculate_hotel_cost(nights: int, cost_per_night: float) -> str:
    """Calculate the total hotel cost."""
    return f"{nights * cost_per_night:.2f}"


@tool
def calculate_food_cost(days: int, cost_per_day: float) -> str:
    """Calculate the total food cost."""
    return f"{days * cost_per_day:.2f}"


travel = float(calculate_travel_cost.invoke({
    "distance_km": 300,
    "cost_per_km": 12
}))

hotel = float(calculate_hotel_cost.invoke({
    "nights": 2,
    "cost_per_night": 1500
}))

food = float(calculate_food_cost.invoke({
    "days": 3,
    "cost_per_day": 500
}))

total = travel + hotel + food

print(f"Travel cost: ₹{travel:.2f}")
print(f"Hotel cost: ₹{hotel:.2f}")
print(f"Food cost: ₹{food:.2f}")
print(f"Total trip cost: ₹{total:.2f}")
