from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from app.schemas.post import PostRead

class UserBase(BaseModel):
    """ Базовая схема пользователя с уникальными данными. """
    email: EmailStr  # Автоматически проверяет валидность формата почты (наличие @, домена)
    username: str

class UserCreate(UserBase):
    """ Схема для регистрации. Только здесь мы принимаем чистый пароль от пользователя. """
    password: str

class UserRead(UserBase):
    """ Схема профиля пользователя для отдачи в API. Пароль сюда не включается в целях безопасности! """
    id: int
    role_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserDetailRead(UserRead):
    """ Схема расширенного профиля. Показывает пользователя вместе со списком его постов. """
    posts: list[PostRead] = []

    model_config = ConfigDict(from_attributes=True)