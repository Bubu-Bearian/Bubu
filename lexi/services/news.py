from typing import List

from lexi.config import get_settings


async def top_headlines(topic: str | None = None) -> List[str]:
    """
    Return sample headlines. Wire to NewsAPI, Google News, or RSS later.
    """
    settings = get_settings()
    sample = [
        "Tech stocks rally as markets hit new highs",
        "Scientists announce breakthrough in battery density",
        "Local city council approves green infrastructure plan",
    ]
    if topic:
        return [f"{topic.title()} update: {headline}" for headline in sample[:2]]
    return sample
