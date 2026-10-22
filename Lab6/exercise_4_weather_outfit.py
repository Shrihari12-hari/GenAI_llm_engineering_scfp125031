
from langchain_core.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get sample weather information for a city."""
    weather_data = {
        "Mumbai": "Hot and humid, 32°C",
        "Pune": "Cloudy, 25°C",
        "Delhi": "Sunny, 30°C",
        "Bengaluru": "Rainy, 22°C"
    }

    return weather_data.get(city.title(), "Weather data unavailable")


@tool
def recommend_outfit(weather: str) -> str:
    """Recommend clothing based on weather information."""
    weather = weather.lower()

    if "rainy" in weather:
        return "Carry an umbrella and wear a raincoat."
    elif "hot" in weather or "humid" in weather or "32°" in weather:
        return "Wear light cotton clothes and stay hydrated."
    elif "cold" in weather:
        return "Wear warm clothes and a jacket."
    else:
        return "Wear comfortable clothes and carry a light jacket."


city = input("Enter city name: ")

weather = get_weather.invoke({"city": city})
print("\nWeather:", weather)

outfit = recommend_outfit.invoke({"weather": weather})
print("Outfit recommendation:", outfit)
