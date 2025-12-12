from __future__ import annotations

import json
from typing import Tuple

from openai import AsyncOpenAI

from lexi.config import get_settings
from lexi.services import calendar, news, web
from lexi.services.memory import MemoryStore

SYSTEM_PROMPT = "You are L.E.X.I, a proactive executive assistant."

TOOLS = {
    "get_calendar": {
        "description": "Fetch today's calendar events",
        "handler": lambda: calendar.today_events(),
    },
    "get_news": {
        "description": "Read current headlines",
        "handler": lambda topic=None: news.top_headlines(topic),
    },
    "web_search": {
        "description": "Search the web",
        "handler": lambda query: web.search(query),
    },
}


async def chat_with_tools(
    user_text: str, *, context: str, memory: MemoryStore
) -> Tuple[str, list[dict]]:
    """Very small orchestrator that can fall back to stubbed replies."""

    settings = get_settings()
    actions: list[dict] = []

    if settings.openai_api_key:
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"Context: {context}"},
            {"role": "user", "content": user_text},
        ]
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        reply = response.choices[0].message.content or "Okay."
    else:
        reply = fallback_response(user_text, context)

    # Naively infer tool calls from keywords
    if "calendar" in user_text.lower():
        events = TOOLS["get_calendar"]["handler"]()
        actions.append({"tool": "get_calendar", "result": events})
    if "news" in user_text.lower() or "headlines" in user_text.lower():
        results = await TOOLS["get_news"]["handler"](None)
        actions.append({"tool": "get_news", "result": results})
    if "search" in user_text.lower():
        results = await TOOLS["web_search"]["handler"](user_text)
        actions.append({"tool": "web_search", "result": results})

    if actions:
        action_summary = json.dumps(actions, indent=2)
        reply += f"\n\nI also fetched this info: {action_summary}"

    memories = await memory.search_memories(user_text)
    if memories:
        reply += "\n\nRecent memory recall:\n" + "\n".join(memories)

    return reply, actions


def fallback_response(user_text: str, context: str) -> str:
    return (
        "(offline mode) I captured your request and will respond with stubbed data. "
        f"You said: '{user_text}'. Context: {context or 'none'}"
    )
