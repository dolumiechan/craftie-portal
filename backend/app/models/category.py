from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class InterestCategory(Base):
    """
    Справочник категорий интересов (например: Рисование, рукоделие, музыка).
    Используется для группировки и фильтрации ленты публикаций по ТЗ.
    """
    __tablename__ = "interest_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)

    # Список всех постов, опубликованных в рамках данной категории
    posts = relationship("Post", back_populates="category")