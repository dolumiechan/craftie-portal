from sqlalchemy.orm import Session
from app.models.user_log import UserLog

def log_user_action(db: Session, user_id: int, action: str, details: str = None) -> UserLog:
    """
    Системный сервис сквозного логирования.
    
    Автоматически фиксирует ключевые действия пользователей и администрации в базу данных
    для последующего аудита безопасности и контроля модерации контента.
    
    :param db: Сессия связи с базой данных SQLAlchemy.
    :param user_id: ID пользователя или администратора, совершившего действие.
    :param action: Строковый код действия (например, 'BLOCKED', 'EXPORT_CSV', 'DELETE_POST').
    :param details: Дополнительное текстовое описание действия (опционально).
    """
    # Создаем экземпляр модели лога, передавая параметры в соответствии со структурой таблицы
    db_log = UserLog(
        user_id=user_id, 
        action=action, 
        details=details
    )
    
    # Сохраняем запись в базу данных
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    
    return db_log