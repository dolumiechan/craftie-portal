from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional
from app.schemas.post import PostFeedRead


class AdminUserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    role_name: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AdminLogRead(BaseModel):
    id: int
    user_id: int
    actor_username: Optional[str] = None
    action: str
    details: Optional[str] = None
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class AdminPostListResponse(BaseModel):
    items: list[PostFeedRead]
    total: int
