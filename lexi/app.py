from fastapi import FastAPI
from pydantic import BaseModel

from lexi.config import get_settings
from lexi.services.llm import chat_with_tools
from lexi.services.memory import MemoryStore
from lexi.jobs.scheduler import build_daily_briefing


app = FastAPI(title="L.E.X.I", description="Voice-first executive assistant API")

settings = get_settings()
memory = MemoryStore()


class ChatRequest(BaseModel):
    session_id: str
    text: str


class ChatResponse(BaseModel):
    reply: str
    actions: list[dict]


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatRequest) -> ChatResponse:
    context = await memory.get_session_context(message.session_id)
    reply, actions = await chat_with_tools(message.text, context=context, memory=memory)
    await memory.store_interaction(message.session_id, message.text, reply)
    return ChatResponse(reply=reply, actions=actions)


@app.get("/briefing")
async def daily_briefing() -> dict:
    """Return a structured daily briefing using calendar + news stubs."""
    briefing = await build_daily_briefing(memory=memory)
    return {"briefing": briefing}


@app.get("/health")
async def healthcheck() -> dict:
    return {"status": "ok", "has_openai_key": settings.openai_api_key is not None}
