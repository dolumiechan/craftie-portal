from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Like(Base):
    """
    Таблица лайков для постов.
    Нужна для реализации системы рейтинга творческих работ.
    """
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    
    # Связь с постом, которому поставили лайк
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    
    # Связь с пользователем, который нажал на кнопку лайка
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Дата и время, когда был поставлен лайк
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # === Связи с другими таблицами ===
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

    # === Системные ограничения базы данных ===
    # Ограничение: один пользователь может поставить только один лайк на конкретный пост.
    # Предотвращает баги с "накруткой" рейтинга от одного и того же человека.
    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="unique_user_post_like"),
    )