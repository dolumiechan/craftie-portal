from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.post import Post
from app.models.like import Like

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/{post_id}")
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    existing = (
        db.query(Like)
        .filter(Like.post_id == post_id, Like.user_id == current_user.id)
        .first()
    )
    if existing:
        return {"message": "Лайк уже поставлен"}

    db.add(Like(post_id=post_id, user_id=current_user.id))
    db.commit()
    return {"message": "Лайк поставлен"}

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    like = (
        db.query(Like)
        .filter(Like.post_id == post_id, Like.user_id == current_user.id)
        .first()
    )
    if not like:
        raise HTTPException(status_code=404, detail="Лайк не найден")

    db.delete(like)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)