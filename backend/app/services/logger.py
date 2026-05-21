<<<<<<< HEAD
from sqlalchemy.orm import Session
from app.models.user_log import UserLog

def log_user_action(db: Session, user_id: int, action_text: str) -> UserLog:
    """Автоматически создает запись аудита для действий пользователя"""
    db_log = UserLog(user_id=user_id, action=action_text)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
=======
from sqlalchemy.orm import Session
from app.models.user_log import UserLog

def log_user_action(db: Session, user_id: int, action_text: str) -> UserLog:
    """Автоматически создает запись аудита для действий пользователя"""
    db_log = UserLog(user_id=user_id, action=action_text)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
>>>>>>> 8d6cb81 (Add posts filtering/search with pagination and implement admin endpoints)
    return db_log