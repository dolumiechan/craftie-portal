from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Comment(Base):
    """
    Таблица комментариев к постам.
    Позволяет пользователям обсуждать опубликованные творческие работы.
    """
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    
    # Связь с постом. Если пост удаляется, все комментарии к нему удаляются автоматически (CASCADE)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    
    # Связь с автором комментария. Если пользователь удален, его комментарии тоже стираются
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Текст комментария (используем Text, так как длина сообщения может быть большой)
    text = Column(Text, nullable=False)
    
    # Дата и время написания комментария, проставляются базой данных автоматически
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # === Связи с другими таблицами ===
    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")