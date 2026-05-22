import os
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User

# Настройки безопасности
SECRET_KEY = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY_KEEP_IT_SAFE_1234567890")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Нахождение эндпоинта для входа
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def hash_password(password: str) -> str:
    """
    Превращает обычный текстовый пароль в защищенный хэш.
    Нужно, чтобы не хранить пароли пользователей в открытом виде.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, совпадает ли введенный пользователем пароль с хэшем из базы данных.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создает временный JWT-токен для авторизации пользователя.
    В токен записывается время, когда его срок действия истечет.
    """
    to_encode = data.copy()
    # Считаем время удаления токена (текущее время + 60 минут)
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Функция-помощник для защиты эндпоинтов.
    Она берет токен из заголовка, проверяет его и возвращает текущего пользователя из базы.
    Если токен сломан или устарел - выдает ошибку 401.
    """
    error_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный токен или срок действия истек",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Расшифровываем токен и берем оттуда email пользователя
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise error_exception
    except jwt.PyJWTError:
        raise error_exception
        
    # Ищем этого пользователя в базе данных
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise error_exception
        
    return user