from pymongo import MongoClient, ASCENDING
from pymongo.database import Database

from config import settings


_client = MongoClient(settings.mongo_uri)
_db: Database = _client[settings.mongo_db_name]


def get_db() -> Database:
    return _db


def init_indexes() -> None:
    _db.users.create_index([("uid", ASCENDING)], unique=True)
    _db.users.create_index([("email", ASCENDING)], sparse=True)
    _db.news.create_index([("title", ASCENDING)], unique=True)
    _db.news.create_index([("country", ASCENDING), ("category", ASCENDING), ("publishedAt", ASCENDING)])
    _db.ads.create_index([("advertiserId", ASCENDING), ("status", ASCENDING)])
    _db.ad_events.create_index([("adId", ASCENDING), ("eventType", ASCENDING), ("createdAt", ASCENDING)])
