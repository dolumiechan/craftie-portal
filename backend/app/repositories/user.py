from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def create_user(self, db: Session, user_in: UserCreate, hashed_password: str) -> User:
        db_user = User(
            email=user_in.email,
            username=user_in.username,
            password_hash=hashed_password,
            role_id=1 # 1 - это обычный пользователь по умолчанию
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

user_repo = UserRepository(User)