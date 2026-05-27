import httpx

from app.config import get_settings

OPENAI_URL = "https://api.openai.com/v1/chat/completions"


def rule_based_reply(message: str) -> str:
    text = message.strip().lower()
    if not text:
        return "Please send a non-empty message."
    if any(word in text for word in ("hello", "hi", "namaste")):
        return "Hello! I am your assignment API assistant. How can I help?"
    if "health" in text:
        return "Use GET /health to check database and Redis status."
    if "bye" in text:
        return "Goodbye! Deploy safely on EC2."
    return f"You said: {message}"


async def generate_reply(message: str):
    """Returns (reply, provider) where provider is 'openai' or 'rules'."""
    settings = get_settings()
    if settings.openai_api_key:
        try:
            reply = await _openai_reply(message, settings.openai_api_key)
            return reply, "openai"
        except (httpx.HTTPError, KeyError, ValueError):
            pass
    return rule_based_reply(message), "rules"


async def _openai_reply(message: str, api_key: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant for a deployment assignment API.",
            },
            {"role": "user", "content": message},
        ],
        "max_tokens": 200,
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(OPENAI_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    return data["choices"][0]["message"]["content"]
