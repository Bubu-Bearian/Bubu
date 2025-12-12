from typing import List


async def search(query: str) -> List[str]:
    """Return pretend web results; plug in SerpAPI/Brave later."""
    return [
        f"Result for '{query}' #1",
        f"Result for '{query}' #2",
        f"Result for '{query}' #3",
    ]
