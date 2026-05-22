from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    """
    Репозиторий для управления данными пользователей.
    Наследует общие методы из BaseRepository и добавляет специфичную логику для пользователей.
    """
    
    def create_user(self, db: Session, user_in: UserCreate, hashed_password: str) -> User:
        """
        Создает и сохраняет нового пользователя в базе данных (Регистрация).
        
        user_in - входные данные от фронтенда (email, username).
        hashed_password - уже зашифрованный в целях безопасности пароль.
        """
        db_user = User(
            email=user_in.email,
            username=user_in.username,
            password_hash=hashed_password,
            role_id=1 # По умолчанию при регистрации каждому новому аккаунту выдается ID роли 1 (Обычный пользователь)
        )
        # Добавляем объект в сессию базы данных
        db.add(db_user)
        # Фиксируем транзакцию (сохраняем изменения на жесткий диск)
        db.commit()
        # Обновляем объект, чтобы считать из базы сгенерированный ID и дату регистрации
        db.refresh(db_user)
        
        return db_user

# Создаем экземпляр репозитория для работы в роутерах
user_repo = UserRepository(User)