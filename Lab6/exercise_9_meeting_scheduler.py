
from langchain_core.tools import tool


@tool
def check_availability(date: str, time: str) -> str:
    """Check whether a meeting time is available."""
    if time in ["10:00", "14:00", "16:00"]:
        return f"{date} at {time} is available."
    return f"{date} at {time} is unavailable."


@tool
def schedule_meeting(name: str, date: str, time: str) -> str:
    """Schedule a meeting with a person."""
    return f"Meeting scheduled with {name} on {date} at {time}."


@tool
def cancel_meeting(name: str, date: str) -> str:
    """Cancel a meeting with a person."""
    return f"Meeting with {name} on {date} has been cancelled."


print(check_availability.invoke({
    "date": "2026-10-25",
    "time": "14:00"
}))

print(schedule_meeting.invoke({
    "name": "Rahul",
    "date": "2026-10-25",
    "time": "14:00"
}))

print(cancel_meeting.invoke({
    "name": "Rahul",
    "date": "2026-10-25"
}))
