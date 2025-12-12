from datetime import datetime

from lexi.services import calendar, news
from lexi.services.memory import MemoryStore


async def build_daily_briefing(memory: MemoryStore) -> str:
    events = calendar.today_events()
    headlines = await news.top_headlines()
    recent = await memory.search_memories("briefing")

    event_lines = "\n".join(f"- {e['time']}: {e['summary']} ({e['location']})" for e in events)
    news_lines = "\n".join(f"- {h}" for h in headlines)
    recall = "\n".join(recent) if recent else "No recent briefing notes stored."

    return (
        f"Good {time_of_day()}, here is your briefing:\n\n"
        f"Calendar:\n{event_lines}\n\n"
        f"Headlines:\n{news_lines}\n\n"
        f"Recent notes:\n{recall}"
    )


def time_of_day() -> str:
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "morning"
    if 12 <= hour < 18:
        return "afternoon"
    return "evening"
