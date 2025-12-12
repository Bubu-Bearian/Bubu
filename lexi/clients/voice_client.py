"""Toy CLI loop for voice interactions.

This does not implement wake-word detection; it simply simulates
record/transcribe/chat/tts.
"""

import asyncio
import sys

import httpx

API_URL = "http://localhost:8000/chat"


async def main() -> None:
    print("Press Ctrl+C to exit. Type your message and press enter.")
    async with httpx.AsyncClient() as client:
        while True:
            try:
                text = input("You: ").strip()
            except KeyboardInterrupt:
                print("\nBye!")
                break

            if not text:
                continue

            payload = {"session_id": "local-cli", "text": text}
            resp = await client.post(API_URL, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            print(f"L.E.X.I: {data['reply']}")
            if data.get("actions"):
                print(f"\nActions taken: {data['actions']}\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
