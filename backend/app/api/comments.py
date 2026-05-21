<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.comment import Comment
from app.models.post import Post
from app.schemas.comment import CommentCreate, CommentRead

router = APIRouter(prefix="/posts", tags=["Comments"])

@router.get("/{id}/comments/", response_model=List[CommentRead])
def list_comments(id: int, db: Session = Depends(get_db)):
    # Проверяем, существует ли пост
    if not db.query(Post).filter(Post.id == id).first():
        raise HTTPException(status_code=404, detail="Пост не найден")
    return db.query(Comment).filter(Comment.post_id == id).all()

@router.post("/{id}/comments/", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(id: int, comment_in: CommentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db.query(Post).filter(Post.id == id).first():
        raise HTTPException(status_code=404, detail="Пост не найден")
        
    new_comment = Comment(text=comment_in.text, post_id=id, user_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
=======
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.comment import Comment
from app.models.post import Post
from app.schemas.comment import CommentCreate, CommentRead

router = APIRouter(prefix="/posts", tags=["Comments"])

@router.get("/{id}/comments/", response_model=List[CommentRead])
def list_comments(id: int, db: Session = Depends(get_db)):
    # Проверяем, существует ли пост
    if not db.query(Post).filter(Post.id == id).first():
        raise HTTPException(status_code=404, detail="Пост не найден")
    return db.query(Comment).filter(Comment.post_id == id).all()

@router.post("/{id}/comments/", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(id: int, comment_in: CommentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db.query(Post).filter(Post.id == id).first():
        raise HTTPException(status_code=404, detail="Пост не найден")
        
    new_comment = Comment(text=comment_in.text, post_id=id, user_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
>>>>>>> 8d6cb81 (Add posts filtering/search with pagination and implement admin endpoints)
    return new_comment