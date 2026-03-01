from fastapi import APIRouter, Depends

from auth import require_role
from database import get_db

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
async def platform_stats(current_user: dict = Depends(require_role("admin"))):
    db = get_db()
    return {
        "users": db.users.count_documents({}),
        "news": db.news.count_documents({}),
        "ads": db.ads.count_documents({}),
        "activeAds": db.ads.count_documents({"status": "active"}),
    }
