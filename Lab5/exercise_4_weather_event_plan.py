
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from datetime import date, timedelta
import requests
import os
import json

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


class EventDetails(BaseModel):
    event_type: str
    event_date: str = Field(
        description="Event date in YYYY-MM-DD format. Resolve relative dates using today's date."
    )
    location: str
    indoor_outdoor_preference: str


class WeatherData(BaseModel):
    temperature: float
    precipitation_chance: int
    conditions: str


parser = PydanticOutputParser(pydantic_object=EventDetails)

today = date.today()

prompt = PromptTemplate(
    template=(
        "Extract the event type, date, location, and indoor/outdoor preference.\n"
        "Today's date is {today}.\n"
        "IMPORTANT: Return event_date strictly as YYYY-MM-DD. "
        "If the description says a weekday such as Saturday, choose the next "
        "occurrence of that weekday on or after today. "
        "If the date is unclear, ask the user rather than inventing a date.\n"
        "Event description: {description}\n"
        "{format_instructions}"
    ),
    input_variables=["description", "today"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

chain = prompt | llm | parser

description = input("Enter event description: ")
event = chain.invoke({
    "description": description,
    "today": today.isoformat()
})

print("\nStep 1: Event Details")
print(event.model_dump_json(indent=2))

# Validate the date before sending it to the weather API.
try:
    event_date = date.fromisoformat(event.event_date)
except ValueError:
    raise ValueError(
        f"Invalid event date: {event.event_date!r}. "
        "Use YYYY-MM-DD, for example 2026-10-24."
    )

if event_date < today:
    raise ValueError(
        f"The event date {event_date} is in the past. "
        "Please enter a future event date."
    )

# Find the location coordinates.
geo = requests.get(
    "https://geocoding-api.open-meteo.com/v1/search",
    params={"name": event.location, "count": 1},
    timeout=20
)
geo.raise_for_status()
places = geo.json().get("results", [])

if not places:
    raise ValueError(
        "Location not found. Enter a more specific city or town."
    )

place = places[0]

# Fetch the forecast for the requested date.
weather = requests.get(
    "https://api.open-meteo.com/v1/forecast",
    params={
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "daily": (
            "temperature_2m_max,"
            "precipitation_probability_max,"
            "weather_code"
        ),
        "timezone": "auto",
        "start_date": event_date.isoformat(),
        "end_date": event_date.isoformat()
    },
    timeout=20
)
weather.raise_for_status()
daily = weather.json().get("daily", {})

if not daily.get("time"):
    raise ValueError(
        "Weather forecast is unavailable for that date. "
        "Try a date within the API's forecast range."
    )

code = daily["weather_code"][0]

conditions = (
    "Clear" if code == 0 else
    "Mainly clear, partly cloudy, or overcast" if code in [1, 2, 3] else
    "Foggy" if code in [45, 48] else
    "Rain or showers" if code in range(51, 83) else
    "Snow or other frozen precipitation" if code in range(71, 78) or code in [85, 86] else
    "Thunderstorm or other severe conditions" if code >= 95 else
    "Other precipitation"
)

data = WeatherData(
    temperature=daily["temperature_2m_max"][0],
    precipitation_chance=daily["precipitation_probability_max"][0],
    conditions=conditions
)

print("\nStep 2: Weather Data")
print(data.model_dump_json(indent=2))

prompt3 = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an event planning assistant. Recommend whether to proceed, "
        "reschedule, or move indoors. Use the event and weather data. "
        "Explain your reasoning briefly. Treat the forecast as guidance, "
        "not a guarantee, and do not invent weather details."
    ),
    (
        "human",
        "Event: {event}\nWeather: {weather}\n"
        "Give a practical recommendation."
    )
])

chain3 = prompt3 | llm | StrOutputParser()

recommendation = chain3.invoke({
    "event": event.model_dump_json(),
    "weather": data.model_dump_json()
})

print("\nStep 3: Event Recommendation")
print(recommendation)
