from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
from typing import Optional, Literal
from app.schemas.post import PostRead
from app.schemas.category import InterestCategoryRead


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class UserRead(UserBase):
    id: int
    role_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserMeRead(UserRead):
    role_name: Optional[str] = None
    is_active: bool = True
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserDetailRead(UserRead):
    role_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    interests: list[InterestCategoryRead] = []
    posts: list[PostRead] = []

    model_config = ConfigDict(from_attributes=True)


class UserRoleUpdate(BaseModel):
    role: Literal["user", "moderator", "admin"]
