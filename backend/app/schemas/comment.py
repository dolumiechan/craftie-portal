from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class CommentBase(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: int
    post_id: int
    user_id: int
    author_username: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommentHistoryRead(CommentBase):
    id: int
    post_id: int
    post_title: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
