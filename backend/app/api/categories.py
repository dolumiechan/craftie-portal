from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.permissions import verify_admin
from app.models.user import User
from app.models.category import InterestCategory as Category
from app.models.post import Post
from app.schemas.category import InterestCategoryCreate as CategoryCreate
from app.schemas.category import InterestCategoryRead as CategoryRead
from app.schemas.category import InterestCategoryUpdate as CategoryUpdate
from app.services.logger import log_user_action

router = APIRouter(prefix="/categories", tags=["Категории интересов"])


@router.get("/", response_model=List[CategoryRead])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.name).all()


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    category_in: CategoryCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(verify_admin),
):
    existing = db.query(Category).filter(Category.name == category_in.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Категория с таким названием уже существует")

    new_category = Category(name=category_in.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    log_user_action(db, user_id=admin.id, action="CREATE_CATEGORY", details=f"id={new_category.id}")
    return new_category


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    category_in: CategoryUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(verify_admin),
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")

    duplicate = (
        db.query(Category)
        .filter(Category.name == category_in.name, Category.id != category_id)
        .first()
    )
    if duplicate:
        raise HTTPException(status_code=400, detail="Категория с таким названием уже существует")

    category.name = category_in.name
    db.commit()
    db.refresh(category)
    log_user_action(db, user_id=admin.id, action="UPDATE_CATEGORY", details=f"id={category_id}")
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(verify_admin),
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")

    posts_count = db.query(Post).filter(Post.category_id == category_id).count()
    if posts_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Нельзя удалить: {posts_count} публикаций используют эту категорию",
        )

    db.delete(category)
    db.commit()
    log_user_action(db, user_id=admin.id, action="DELETE_CATEGORY", details=f"id={category_id}")
    return None
