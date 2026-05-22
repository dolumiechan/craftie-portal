from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base

# ВСПОМОГАТЕЛЬНАЯ ТАБЛИЦА СВЯЗИ (Многие-ко-Многим)
# Нужна, чтобы связать посты и теги. У одного поста может быть много тегов, 
# и один тег может использоваться во множестве разных постов.
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)

class Tag(Base):
    """
    Таблица тегов (меток) для постов.
    Помогает группировать и искать публикации по определенным темам (например: #рисунок, #дизайн).
    """
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    
    # Название тега. Оно должно быть уникальным, чтобы теги не дублировались в базе
    name = Column(String(50), unique=True, nullable=False, index=True)

    # Связь с постами через вспомогательную таблицу post_tags
    posts = relationship("Post", secondary=post_tags, back_populates="tags")