from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.category import InterestCategory as Category
from app.schemas.category import InterestCategoryCreate as CategoryCreate
from app.schemas.category import InterestCategoryRead as CategoryRead

router = APIRouter(prefix="/categories", tags=["Категории интересов"])


def verify_admin(current_user: User = Depends(get_current_user)):
    """Вспомогательная функция для проверки прав администратора."""
    # Раскрываем объект связи role и проверяем текстовое имя роли
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Данное действие доступно только администратору системы"
        )
    return current_user


@router.get("/", response_model=List[CategoryRead])
def get_categories(db: Session = Depends(get_db)):
    """
    Получение списка всех категорий интересов.
    Используется для построения меню фильтрации и при публикации работ.
    """
    return db.query(Category).all()


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    category_in: CategoryCreate, 
    db: Session = Depends(get_db), 
    admin: User = Depends(verify_admin)  # Используем зависимость
):
    """
    Создание новой категории интересов.
    Доступно исключительно администратору. Проверяет уникальность имени категории.
    """
    # Проверка на дубликат названия
    existing = db.query(Category).filter(Category.name == category_in.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Категория с таким названием уже существует"
        )
        
    new_category = Category(name=category_in.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category