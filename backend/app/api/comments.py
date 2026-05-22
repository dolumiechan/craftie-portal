from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.comment import Comment
from app.models.post import Post
from app.schemas.comment import CommentCreate, CommentRead
from app.services.logger import log_user_action as log_action  # Подключаем логирование

router = APIRouter(prefix="/posts", tags=["Комментарии"])


@router.get("/{id}/comments/", response_model=List[CommentRead])
def list_comments(id: int, db: Session = Depends(get_db)):
    """
    Просмотр списка комментариев к конкретной публикации.
    Доступен всем пользователям, включая неавторизованных.
    """
    # Проверяем, существует ли целевой пост
    if not db.query(Post).filter(Post.id == id).first():
        raise HTTPException(status_code=404, detail="Пост не найден")
        
    return db.query(Comment).filter(Comment.post_id == id).all()


@router.post("/{id}/comments/", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(
    id: int, 
    comment_in: CommentCreate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Добавление комментария под публикацией.
    Доступно только для авторизованных пользователей.
    """
    if not db.query(Post).filter(Post.id == id).first():
        raise HTTPException(status_code=404, detail="Пост не найден")
        
    new_comment = Comment(text=comment_in.text, post_id=id, user_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Удаление комментария.
    Права доступа:
    1. Автор комментария может удалить только свой комментарий.
    2. Модератор или Администратор могут удалить ЛЮБОЙ комментарий.
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")

    # Проверяем роли и авторство
    is_author = comment.user_id == current_user.id
    is_staff = current_user.role and current_user.role.name in ["moderator", "admin"]

    if not is_author and not is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для удаления этого комментария."
        )

    # Если удаляет представитель администрации - логируем это действие модерации
    if is_staff and not is_author:
        log_action(
            db, 
            user_id=current_user.id, 
            action="MODERATE_DELETE_COMMENT", 
            details=f"Удален чужой комментарий ID={comment.id} пользователя ID={comment.user_id}"
        )

    db.delete(comment)
    db.commit()
    return None