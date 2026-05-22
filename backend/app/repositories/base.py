from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from app.core.database import Base

# Создаем гибкий тип данных для моделей
ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    Базовый репозиторий с общими методами для всех таблиц.
    
    Избавляет от дублирования кода. Любой новый репозиторий, унаследованный от этого, 
    сразу получает готовые функции поиска по ID и вывода списком.
    """
    def __init__(self, model: Type[ModelType]):
        """
        Принимает модель SQLAlchemy, с которой будет работать репозиторий (например, User или Post).
        """
        self.model = model

    def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        """
        Ищет одну запись в базе данных по её уникальному идентификатору (ID).
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Возвращает список записей из таблицы с поддержкой пагинации.
        skip — сколько записей пропустить с начала (для переключения страниц).
        limit — максимальное количество записей на одной странице.
        """
        return db.query(self.model).offset(skip).limit(limit).all()