# L.E.X.I prototype

A small FastAPI-based skeleton for a voice-first assistant with memory, news/calendar tools, and a CLI client.

## Quickstart
1. Install dependencies: `pip install -r requirements.txt`.
2. Run the API: `uvicorn lexi.app:app --reload`.
3. In another terminal, run the CLI client: `python -m lexi.clients.voice_client`.

Set `OPENAI_API_KEY` to enable real LLM responses; otherwise a stubbed offline reply is used.

## Features
- `/chat` endpoint that keeps session context and can trigger calendar/news/web tools.
- `/briefing` endpoint that synthesizes a daily briefing from stubbed data.
- Simple in-memory memory store with recall hooks.
- CLI loop demonstrating the interaction pattern.

Replace the stub implementations in `lexi/services` with production integrations (Redis/pgvector, News API, Google/Microsoft Calendar, etc.).
