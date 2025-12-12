from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class MemoryStore:
    """Naive in-memory store. Replace with Redis/pgvector in production."""

    _short_term: Dict[str, str] = field(default_factory=dict)
    _long_term: List[str] = field(default_factory=list)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    async def get_session_context(self, session_id: str) -> str:
        async with self._lock:
            return self._short_term.get(session_id, "")

    async def store_interaction(self, session_id: str, user: str, bot: str) -> None:
        transcript = f"User: {user}\nL.E.X.I: {bot}"
        async with self._lock:
            self._short_term[session_id] = transcript
            self._long_term.append(transcript)

    async def search_memories(self, query: str, limit: int = 3) -> list[str]:
        """Return the most recent snippets containing keywords."""
        async with self._lock:
            matches = [m for m in reversed(self._long_term) if query.lower() in m.lower()]
        return list(matches)[:limit]
