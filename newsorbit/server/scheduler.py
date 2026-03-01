import asyncio
import logging

from apscheduler.schedulers.background import BackgroundScheduler

from database import get_db
from utils.gemini import analyze_article
from utils.news_fetcher import fetch_gnews

logger = logging.getLogger("scheduler")
scheduler = BackgroundScheduler()


async def _refresh_active_countries() -> None:
    db = get_db()
    countries = db.users.distinct("country") or ["us"]
    categories = ["general", "business", "technology", "sports"]

    for country in countries:
        for category in categories:
            articles = await fetch_gnews(country, category, max_items=8)
            for article in articles:
                try:
                    ai = await analyze_article(article)
                    if int(ai.get("importance", 0)) <= 6:
                        continue
                    db.news.update_one(
                        {"title": article.get("title", "")},
                        {
                            "$setOnInsert": {
                                "title": article.get("title", ""),
                                "summary": ai.get("summary", ""),
                                "country": country,
                                "category": category,
                                "sentiment": ai.get("sentiment", "neutral"),
                                "importance": int(ai.get("importance", 0)),
                                "tags": ai.get("tags", []),
                                "publishedAt": article.get("publishedAt"),
                                "source": (article.get("source") or {}).get("name", "Unknown"),
                                "originalUrl": article.get("url"),
                                "rewrittenHeadline": ai.get("rewrittenHeadline", article.get("title", "")),
                            }
                        },
                        upsert=True,
                    )
                except Exception as ex:  # noqa: BLE001
                    logger.exception("scheduler processing failure: %s", ex)


def scheduled_refresh_news() -> None:
    asyncio.run(_refresh_active_countries())


def start_scheduler() -> None:
    scheduler.add_job(scheduled_refresh_news, "interval", minutes=30, id="news-refresh", replace_existing=True)
    scheduler.start()
