from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.schemas.post_image import PostImageRead
from app.schemas.category import InterestCategoryRead

class PostBase(BaseModel):
    title: str
    description: Optional[str] = None
    category_id: Optional[int] = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None

class PostRead(PostBase):
    id: int
    author_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PostDetailRead(PostRead):
    category: Optional[InterestCategoryRead] = None
    images: List[PostImageRead] = []

    model_config = ConfigDict(from_attributes=True)