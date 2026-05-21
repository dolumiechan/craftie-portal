from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.post import Post
from app.schemas.post import PostCreate, PostRead, PostDetailRead, PostUpdate

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=List[PostRead])
def list_posts(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return db.query(Post).offset(skip).limit(limit).all()

@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(post_in: PostCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_post = Post(**post_in.model_dump(), author_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=PostDetailRead)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    return post

@router.put("/{id}", response_model=PostRead)
def update_post(id: int, post_update: PostUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав на редактирование этого поста")
        
    for key, value in post_update.model_dump(exclude_unset=True).items():
        setattr(post, key, value)
        
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    
    # ПРОВЕРКА ПРАВ: Удалить может либо сам автор, либо модератор/админ
    is_author = post.author_id == current_user.id
    is_staff = current_user.role and current_user.role.name in ["moderator", "admin"]
    
    if not is_author and not is_staff:
        raise HTTPException(
            status_code=403, 
            detail="Нет прав на удаление этого поста. Вы должны быть автором или модератором."
        )
        
    db.delete(post)
    db.commit()
    return None