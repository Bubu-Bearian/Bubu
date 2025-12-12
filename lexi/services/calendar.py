from datetime import datetime
from typing import List, TypedDict


class CalendarEvent(TypedDict):
    summary: str
    time: str
    location: str | None


def today_events() -> List[CalendarEvent]:
    """Stubbed calendar events; wire to Google/Microsoft in production."""
    now = datetime.now().strftime("%Y-%m-%d")
    return [
        {"summary": "Team sync", "time": f"{now} 10:00", "location": "Zoom"},
        {"summary": "Product review", "time": f"{now} 14:00", "location": "Room 3"},
    ]


def book_event(summary: str, time: str, location: str | None = None) -> CalendarEvent:
    return {"summary": summary, "time": time, "location": location}
