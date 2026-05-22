from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.models.user import User, Role
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя в системе.
    
    Выполняет следующие проверки:
    1. Уникальность адреса электронной почты (email).
    2. Уникальность имени пользователя (username).
    
    Автоматически присваивает пользователю базовую роль 'user' из справочника ролей.
    """
    # Проверка уникальности email
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
        
    # Проверка уникальности имени пользователя
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="Это имя пользователя уже занято")
        
    # Запрос базовой роли из базы данных
    user_role = db.query(Role).filter(Role.name == "user").first()
    
    # Создание сущности пользователя с хэшированием пароля
    new_user = User(
        email=user_in.email,
        username=user_in.username,
        password_hash=hash_password(user_in.password),
        # Страховка: если роль 'user' не найдена, ставим по умолчанию id=2 (согласно структуре БД)
        role_id=user_role.id if user_role else 2 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Аутентификация пользователя и генерация сессионного JWT-токена.
    
    Поддерживает авторизацию как по email, так и по имени пользователя через стандартное поле username.
    Проверяет статус блокировки аккаунта.
    """
    # Поиск пользователя по двум альтернативным уникальным полям
    user = db.query(User).filter(
        (User.email == form_data.username) | (User.username == form_data.username)
    ).first()
    
    # Верификация хэша пароля безопасным методом bcrypt
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Неверный email/имя пользователя или пароль"
        )
        
    # Проверка флага активности аккаунта
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ваш аккаунт заблокирован администрацией."
        )
        
    # Генерация токена доступа с указанием идентификатора
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Получение профиля вошедшего пользователя.
    
    Автоматически проверяет JWT-токен в заголовке запроса 
    и возвращает данные текущего авторизованного пользователя.
    """
    return current_user