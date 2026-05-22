from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class UserLog(Base):
    """
    Таблица системных логов (аудита действий).
    Фиксирует важные события: удаления, блокировки, экспорт данных администраторами.
    Необходима для контроля безопасности и модерации.
    """
    __tablename__ = "user_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # ID пользователя или модератора, который совершил действие
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Короткое название действия (например: 'USER_BLOCKED', 'COMMENT_DELETED')
    action = Column(String(255), nullable=False)
    
    # Дополнительные текстовые детали (например: 'Заблокирован пользователь с ID 5 за спам')
    details = Column(String, nullable=True)
    
    # Точная дата и время, когда произошло это событие
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # === Связь с таблицей пользователей ===
    user = relationship("User", back_populates="logs")