from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NewsQuery(BaseModel):
    country: str
    categories: list[str] = Field(default_factory=lambda: ["general"])


class ProcessedNews(BaseModel):
    title: str
    summary: str
    country: str
    category: str
    sentiment: str
    importance: int
    tags: list[str]
    publishedAt: datetime
    source: str
    originalUrl: Optional[str] = None
    rewrittenHeadline: str
