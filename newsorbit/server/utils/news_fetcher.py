from typing import Any

import httpx

from config import settings


GNEWS_URL = "https://gnews.io/api/v4/top-headlines"


async def fetch_gnews(country: str, category: str, max_items: int = 20) -> list[dict[str, Any]]:
    params = {
        "token": settings.gnews_api_key,
        "lang": "en",
        "country": country,
        "topic": category,
        "max": max_items,
    }
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(GNEWS_URL, params=params)
        response.raise_for_status()
        return response.json().get("articles", [])
