from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.models.user import User
from app.repositories.user import user_repo
from app.schemas.user import UserCreate, UserRead, UserMeRead
from app.services.user_mapper import user_to_me_read

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if user_repo.get_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    if user_repo.get_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="Это имя пользователя уже занято")

    return user_repo.create_user(db, user_in, hash_password(user_in.password))


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .options(joinedload(User.role))
        .filter(
            (User.email == form_data.username) | (User.username == form_data.username)
        )
        .first()
    )

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email/username или пароль",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ваш аккаунт заблокирован администрацией.",
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserMeRead)
def get_me(current_user: User = Depends(get_current_user)):
    return user_to_me_read(current_user)
