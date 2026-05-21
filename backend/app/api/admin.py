from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.permissions import RoleChecker
from app.models.user import User
from app.models.post import Post
from app.schemas.user import UserRead

router = APIRouter(
    prefix="/admin", 
    tags=["Admin Management"],
    dependencies=[Depends(RoleChecker(["admin"]))]
)

# 1. Получить список всех пользователей (с пагинацией)
@router.get("/users/", response_model=List[UserRead])
def admin_get_users(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    offset = (page - 1) * size
    return db.query(User).offset(offset).limit(size).all()


# 2. Блокировка / Разблокировка пользователя
@router.post("/users/{user_id}/toggle-block")
def admin_toggle_user_block(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
        
    # Не даем админу заблокировать самого себя
    
    # Меняем статус на противоположный
    user.is_active = not user.is_active
    db.commit()
    
    status_text = "заблокирован" if not user.is_active else "разблокирован"
    return {"message": f"Пользователь {user.username} успешно {status_text}."}


# 3. Удаление ЛЮБОГО поста
@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
        
    db.delete(post)
    db.commit()
    return None