from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.schemas.post_image import PostImageRead
from app.schemas.category import InterestCategoryRead


class PostBase(BaseModel):
    """Базовая схема поста с основной текстовой информацией."""
    title: str
    description: Optional[str] = None
    category_id: Optional[int] = None


class PostCreate(PostBase):
    """Схема, которую присылает пользователь при создании публикации."""
    pass


class PostUpdate(BaseModel):
    """Схема для редактирования поста. Все поля необязательны."""
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None


class PostRead(PostBase):
    """Схема для краткого отображения поста (внутренние операции)."""
    id: int
    author_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostFeedRead(PostBase):
    """Схема карточки в публичной ленте."""
    id: int
    author_id: int
    author_username: str
    category_name: Optional[str] = None
    created_at: datetime
    image_url: Optional[str] = None
    comments_count: int = 0
    is_hidden: bool = False

    model_config = ConfigDict(from_attributes=True)


class PostFeedListResponse(BaseModel):
    """Ответ ленты с пагинацией."""
    items: List[PostFeedRead]
    total: int
    skip: int
    limit: int


class TagRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class PostDetailRead(PostRead):
    """Схема для детального просмотра поста."""
    author_username: str
    category_name: Optional[str] = None
    image_url: Optional[str] = None
    comments_count: int = 0
    category: Optional[InterestCategoryRead] = None
    images: List[PostImageRead] = []
    tags: List[TagRead] = []

    model_config = ConfigDict(from_attributes=True)
