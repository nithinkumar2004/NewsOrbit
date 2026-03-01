from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId

from auth import get_current_user, require_role
from database import get_db
from models.ads_model import AdCreateRequest, AdEventRequest
from utils.ads_engine import track_ad_event

router = APIRouter(prefix="/ads", tags=["ads"])


@router.post("")
async def create_ad(
    payload: AdCreateRequest,
    current_user: dict = Depends(require_role("advertiser", "admin")),
):
    ad = {
        "advertiserId": current_user["uid"],
        "title": payload.title,
        "image": str(payload.image),
        "country": payload.country,
        "category": payload.category,
        "budget": payload.budget,
        "impressions": 0,
        "clicks": 0,
        "spent": 0,
        "cpc": 0.2,
        "status": "active",
        "createdAt": datetime.utcnow(),
    }
    inserted = get_db().ads.insert_one(ad)
    return {"id": str(inserted.inserted_id), "message": "Ad created"}


@router.get("/mine")
async def list_my_ads(current_user: dict = Depends(require_role("advertiser", "admin"))):
    ads = list(get_db().ads.find({"advertiserId": current_user["uid"]}))
    for ad in ads:
        ad["_id"] = str(ad["_id"])
    return ads


@router.post("/track")
async def track(payload: AdEventRequest, current_user: dict = Depends(get_current_user)):
    if payload.eventType not in {"impression", "click"}:
        raise HTTPException(status_code=400, detail="Unsupported event type")
    track_ad_event(payload.adId, payload.eventType)
    return {"message": "Event tracked"}


@router.get("/analytics")
async def analytics(current_user: dict = Depends(require_role("advertiser", "admin"))):
    db = get_db()
    pipeline = [
        {"$match": {"advertiserId": current_user["uid"]}},
        {
            "$group": {
                "_id": None,
                "campaigns": {"$sum": 1},
                "totalImpressions": {"$sum": "$impressions"},
                "totalClicks": {"$sum": "$clicks"},
                "revenue": {"$sum": "$spent"},
            }
        },
    ]
    result = list(db.ads.aggregate(pipeline))
    return result[0] if result else {"campaigns": 0, "totalImpressions": 0, "totalClicks": 0, "revenue": 0}
