
from langchain_core.tools import tool


@tool
def calculate_bmi(weight_kg: float, height_m: float) -> str:
    """Calculate BMI using weight in kilograms and height in meters."""
    if weight_kg <= 0 or height_m <= 0:
        return "Error: Weight and height must be positive."

    bmi = weight_kg / (height_m ** 2)
    return f"BMI: {bmi:.2f}"


@tool
def calculate_daily_calories(weight_kg: float, activity_factor: float) -> str:
    """Estimate daily calories using weight and an activity factor."""
    if weight_kg <= 0 or activity_factor <= 0:
        return "Error: Weight and activity factor must be positive."

    calories = weight_kg * 24 * activity_factor
    return f"Estimated daily calories: {calories:.0f} kcal"


print(calculate_bmi.invoke({
    "weight_kg": 70,
    "height_m": 1.75
}))

print(calculate_daily_calories.invoke({
    "weight_kg": 70,
    "activity_factor": 1.5
}))
