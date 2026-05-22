from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.schemas.post_image import PostImageRead
from app.schemas.category import InterestCategoryRead

class PostBase(BaseModel):
    """ Базовая схема поста с основной текстовой информацией. """
    title: str
    description: Optional[str] = None  # Описание необязательно
    category_id: Optional[int] = None   # Категория может быть не указана

class PostCreate(PostBase):
    """ Схема, которую присылает пользователь при создании публикации. """
    pass

class PostUpdate(BaseModel):
    """ Схема для редактирования поста. Все поля необязательны, можно обновить только часть. """
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None

class PostRead(PostBase):
    """ Схема для краткого отображения поста (например, в ленте). """
    id: int
    author_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PostDetailRead(PostRead):
    """ Схема для детального просмотра поста. Подтягивает связанные картинки и категорию. """
    category: Optional[InterestCategoryRead] = None
    images: List[PostImageRead] = []  # Список картинок поста, по умолчанию пустой

    model_config = ConfigDict(from_attributes=True)