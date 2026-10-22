
from langchain_core.tools import tool


@tool
def find_restaurants(location: str) -> str:
    """Find restaurants in a location."""
    restaurants = {
        "pune": ["Spice Garden", "Green Bowl", "Pizza Corner"],
        "mumbai": ["Coastal Kitchen", "Green Bowl", "Pizza Corner"]
    }

    return ", ".join(restaurants.get(location.lower(), ["No restaurants found"]))


@tool
def filter_by_cuisine(restaurants: str, cuisine: str) -> str:
    """Filter restaurants based on cuisine."""
    cuisine_data = {
        "indian": ["Spice Garden", "Coastal Kitchen"],
        "healthy": ["Green Bowl"],
        "italian": ["Pizza Corner"]
    }

    available = restaurants.split(", ")
    matches = [
        restaurant
        for restaurant in cuisine_data.get(cuisine.lower(), [])
        if restaurant in available
    ]

    return ", ".join(matches) if matches else "No matching restaurants found"


@tool
def filter_by_budget(restaurants: str, budget: float) -> str:
    """Filter restaurants using a maximum budget per person."""
    prices = {
        "Spice Garden": 400,
        "Coastal Kitchen": 600,
        "Green Bowl": 250,
        "Pizza Corner": 350
    }

    available = restaurants.split(", ")
    matches = [
        restaurant
        for restaurant in available
        if restaurant in prices and prices[restaurant] <= budget
    ]

    return ", ".join(matches) if matches else "No restaurants within budget"


@tool
def recommend_restaurant(restaurants: str) -> str:
    """Recommend a restaurant from the provided options."""
    options = restaurants.split(", ")

    if not options or options == [""]:
        return "No restaurant available to recommend."

    return f"Recommended restaurant: {options[0]}"


location = input("Enter city (Pune/Mumbai): ")
cuisine = input("Enter cuisine (Indian/Healthy/Italian): ")
budget = float(input("Enter budget per person in rupees: "))

restaurants = find_restaurants.invoke({"location": location})
print("\nRestaurants:", restaurants)

restaurants = filter_by_cuisine.invoke({
    "restaurants": restaurants,
    "cuisine": cuisine
})
print("After cuisine filter:", restaurants)

restaurants = filter_by_budget.invoke({
    "restaurants": restaurants,
    "budget": budget
})
print("After budget filter:", restaurants)

recommendation = recommend_restaurant.invoke({
    "restaurants": restaurants
})
print(recommendation)

