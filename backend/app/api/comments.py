from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.comment import Comment
from app.models.post import Post
from app.schemas.comment import CommentCreate, CommentRead
from app.services.logger import log_user_action as log_action

router = APIRouter(prefix="/posts", tags=["Комментарии"])


def _comment_to_read(comment: Comment) -> CommentRead:
    return CommentRead(
        id=comment.id,
        text=comment.text,
        post_id=comment.post_id,
        user_id=comment.user_id,
        author_username=comment.author.username if comment.author else None,
        created_at=comment.created_at,
    )


@router.get("/{id}/comments/", response_model=List[CommentRead])
def list_comments(id: int, db: Session = Depends(get_db)):
    if not db.query(Post).filter(Post.id == id).first():
        raise HTTPException(status_code=404, detail="Пост не найден")

    comments = (
        db.query(Comment)
        .options(joinedload(Comment.author))
        .filter(Comment.post_id == id)
        .order_by(Comment.created_at.asc())
        .all()
    )
    return [_comment_to_read(c) for c in comments]


@router.post("/{id}/comments/", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(
    id: int,
    comment_in: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not db.query(Post).filter(Post.id == id).first():
        raise HTTPException(status_code=404, detail="Пост не найден")

    new_comment = Comment(text=comment_in.text, post_id=id, user_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    comment = (
        db.query(Comment)
        .options(joinedload(Comment.author))
        .filter(Comment.id == new_comment.id)
        .first()
    )
    return _comment_to_read(comment)


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")

    is_author = comment.user_id == current_user.id
    is_staff = current_user.role and current_user.role.name in ["moderator", "admin"]

    if not is_author and not is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для удаления этого комментария.",
        )

    if is_staff and not is_author:
        log_action(
            db,
            user_id=current_user.id,
            action="MODERATE_DELETE_COMMENT",
            details=f"comment_id={comment.id} author_id={comment.user_id}",
        )
    else:
        log_action(
            db,
            user_id=current_user.id,
            action="DELETE_OWN_COMMENT",
            details=f"comment_id={comment.id}",
        )

    db.delete(comment)
    db.commit()
    return None
