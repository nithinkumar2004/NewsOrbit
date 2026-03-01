from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class AdCreateRequest(BaseModel):
    title: str
    image: HttpUrl
    country: str
    category: str
    budget: float = Field(..., gt=0)


class AdInDB(BaseModel):
    advertiserId: str
    title: str
    image: str
    country: str
    category: str
    budget: float
    impressions: int = 0
    clicks: int = 0
    spent: float = 0
    cpc: float = 0.2
    status: str = "active"
    createdAt: datetime = Field(default_factory=datetime.utcnow)


class AdEventRequest(BaseModel):
    adId: str
    eventType: str  # impression|click
    newsCategory: Optional[str] = None
