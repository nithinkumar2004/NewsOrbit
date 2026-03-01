import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pymongo.errors import DuplicateKeyError

from auth import get_current_user
from database import get_db
from models.news_model import NewsQuery
from utils.ads_engine import get_matching_ads
from utils.gemini import analyze_article
from utils.news_fetcher import fetch_gnews

router = APIRouter(prefix="/news", tags=["news"])
logger = logging.getLogger("news")


@router.post("/refresh")
async def refresh_news(payload: NewsQuery, current_user: dict = Depends(get_current_user)):
    db = get_db()
    inserted = 0
    for category in payload.categories:
        articles = await fetch_gnews(payload.country, category)
        for article in articles:
            try:
                ai = await analyze_article(article)
                if ai.get("importance", 0) <= 6:
                    continue
                item = {
                    "title": article.get("title", "Untitled"),
                    "summary": ai.get("summary", ""),
                    "country": payload.country,
                    "category": category,
                    "sentiment": ai.get("sentiment", "neutral"),
                    "importance": int(ai.get("importance", 0)),
                    "tags": ai.get("tags", []),
                    "publishedAt": datetime.fromisoformat(article.get("publishedAt", datetime.utcnow().isoformat()).replace("Z", "+00:00")),
                    "source": (article.get("source") or {}).get("name", "Unknown"),
                    "originalUrl": article.get("url"),
                    "rewrittenHeadline": ai.get("rewrittenHeadline", article.get("title", "")),
                }
                db.news.insert_one(item)
                inserted += 1
            except DuplicateKeyError:
                continue
            except Exception as ex:  # noqa: BLE001
                logger.exception("Failed processing article: %s", ex)

    return {"inserted": inserted}


@router.get("")
async def list_news(country: str, category: str = "general", limit: int = 30, current_user: dict = Depends(get_current_user)):
    db = get_db()
    docs = list(
        db.news.find({"country": country, "category": category}, {"_id": 0})
        .sort("publishedAt", -1)
        .limit(limit)
    )
    if not docs:
        raise HTTPException(status_code=404, detail="No news available, refresh first")

    ads = get_matching_ads(country, category, limit=max(1, limit // 5))
    return {"news": docs, "ads": ads}
