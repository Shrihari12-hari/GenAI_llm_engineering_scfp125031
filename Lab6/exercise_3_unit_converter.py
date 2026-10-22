
from langchain_core.tools import tool


@tool
def celsius_to_fahrenheit(celsius: float) -> str:
    """Convert Celsius temperature to Fahrenheit."""
    fahrenheit = (celsius * 9 / 5) + 32
    return f"{celsius}°C = {fahrenheit:.2f}°F"


@tool
def kilometers_to_miles(kilometers: float) -> str:
    """Convert kilometers to miles."""
    miles = kilometers * 0.621371
    return f"{kilometers} km = {miles:.2f} miles"


@tool
def kilograms_to_pounds(kilograms: float) -> str:
    """Convert kilograms to pounds."""
    pounds = kilograms * 2.20462
    return f"{kilograms} kg = {pounds:.2f} pounds"


tools = [
    celsius_to_fahrenheit,
    kilometers_to_miles,
    kilograms_to_pounds
]

print(celsius_to_fahrenheit.invoke({"celsius": 25}))
print(kilometers_to_miles.invoke({"kilometers": 10}))
print(kilograms_to_pounds.invoke({"kilograms": 5}))
