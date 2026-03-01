from datetime import datetime
from bson import ObjectId

from database import get_db


def get_matching_ads(country: str, category: str, limit: int = 5) -> list[dict]:
    db = get_db()
    ads = list(
        db.ads.find(
            {
                "country": country,
                "category": category,
                "status": "active",
                "$expr": {"$lt": ["$spent", "$budget"]},
            },
            {"_id": 0},
        ).limit(limit)
    )
    return ads


def track_ad_event(ad_id: str, event_type: str) -> None:
    db = get_db()
    if not ObjectId.is_valid(ad_id):
        return

    query = {"_id": ObjectId(ad_id)}
    ad = db.ads.find_one(query)
    if not ad:
        return

    updates = {"$set": {"updatedAt": datetime.utcnow()}}
    if event_type == "impression":
        updates["$inc"] = {"impressions": 1}
    elif event_type == "click":
        cpc = float(ad.get("cpc", 0.2))
        next_spent = float(ad.get("spent", 0)) + cpc
        status = "paused" if next_spent >= float(ad.get("budget", 0)) else "active"
        updates["$inc"] = {"clicks": 1, "spent": cpc}
        updates["$set"]["status"] = status
    else:
        return

    db.ads.update_one(query, updates)
    db.ad_events.insert_one({"adId": ad_id, "eventType": event_type, "createdAt": datetime.utcnow()})
