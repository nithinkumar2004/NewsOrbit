from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserInDB(BaseModel):
    uid: str
    name: str = ""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    country: str = "us"
    preferences: list[str] = Field(default_factory=list)
    role: str = "user"
    createdAt: datetime = Field(default_factory=datetime.utcnow)


class UpdateProfileRequest(BaseModel):
    country: str
    preferences: list[str] = Field(default_factory=list)


class UpgradeRoleRequest(BaseModel):
    role: str
