"""Placeholder TTS/STT wrappers."""


async def transcribe_audio(_: bytes) -> str:
    return "(transcription placeholder)"


async def synthesize(text: str) -> bytes:
    return text.encode()
