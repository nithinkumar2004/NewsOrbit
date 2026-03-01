from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from auth import create_access_token, get_current_user, verify_firebase_token
from database import get_db
from models.user_model import UpdateProfileRequest, UpgradeRoleRequest

router = APIRouter(prefix="/auth", tags=["auth"])


class FirebaseLoginRequest(BaseModel):
    idToken: str


@router.post("/firebase-login")
async def firebase_login(payload: FirebaseLoginRequest):
    decoded = verify_firebase_token(payload.idToken)
    uid = decoded.get("uid")
    if not uid:
        raise HTTPException(status_code=400, detail="Invalid Firebase payload")

    db = get_db()
    user = db.users.find_one({"uid": uid}, {"_id": 0})
    if not user:
        user = {
            "uid": uid,
            "name": decoded.get("name", ""),
            "email": decoded.get("email"),
            "phone": decoded.get("phone_number"),
            "country": "us",
            "preferences": [],
            "role": "user",
            "createdAt": datetime.utcnow(),
        }
        db.users.insert_one(user)

    token = create_access_token({"uid": uid, "role": user.get("role", "user")})
    return {"access_token": token, "user": user}


@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    return current_user


@router.put("/profile")
async def update_profile(payload: UpdateProfileRequest, current_user: dict = Depends(get_current_user)):
    db = get_db()
    db.users.update_one(
        {"uid": current_user["uid"]},
        {"$set": {"country": payload.country, "preferences": payload.preferences}},
    )
    return {"message": "Profile updated"}


@router.post("/upgrade-role")
async def upgrade_role(payload: UpgradeRoleRequest, current_user: dict = Depends(get_current_user)):
    if payload.role not in {"user", "advertiser", "admin"}:
        raise HTTPException(status_code=400, detail="Unsupported role")
    get_db().users.update_one({"uid": current_user["uid"]}, {"$set": {"role": payload.role}})
    token = create_access_token({"uid": current_user["uid"], "role": payload.role})
    return {"message": "Role upgraded", "access_token": token}
