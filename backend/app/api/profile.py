import json
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.core.image_service import image_service
from app.core.security import get_current_user
from app.models.user import User
from app.models.category import InterestCategory
from app.models.comment import Comment
from app.schemas.user import UserDetailRead
from app.schemas.comment import CommentHistoryRead
from app.services.post_feed import remove_media_file
from app.services.user_mapper import user_to_detail_read

router = APIRouter(prefix="/profile", tags=["Личный кабинет автора"])

PROFILE_LOAD_OPTIONS = (
    joinedload(User.role),
    joinedload(User.interests),
    joinedload(User.posts),
)


def _load_profile_user(db: Session, user_id: int) -> User:
    user = (
        db.query(User)
        .options(*PROFILE_LOAD_OPTIONS)
        .filter(User.id == user_id)
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


def _sync_interests(db: Session, user: User, interest_ids_json: Optional[str]) -> None:
    if interest_ids_json is None:
        return
    try:
        raw_ids = json.loads(interest_ids_json)
        if not isinstance(raw_ids, list):
            raise ValueError("interest_ids must be a JSON array")
        ids = [int(x) for x in raw_ids]
    except (json.JSONDecodeError, ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Неверный формат interest_ids (ожидается JSON-массив id)")

    if not ids:
        user.interests = []
        return

    categories = db.query(InterestCategory).filter(InterestCategory.id.in_(ids)).all()
    if len(categories) != len(set(ids)):
        raise HTTPException(status_code=400, detail="Одна или несколько категорий не найдены")
    user.interests = categories


@router.get("/", response_model=UserDetailRead)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = _load_profile_user(db, current_user.id)
    return user_to_detail_read(user)


@router.put("/", response_model=UserDetailRead)
def update_profile(
    username: str = Form(...),
    email: str = Form(...),
    bio: Optional[str] = Form(None),
    interest_ids: Optional[str] = Form(None),
    avatar: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = _load_profile_user(db, current_user.id)

    if email != user.email:
        if db.query(User).filter(User.email == email, User.id != user.id).first():
            raise HTTPException(status_code=400, detail="Этот email уже зарегистрирован в системе")

    if username != user.username:
        if db.query(User).filter(User.username == username, User.id != user.id).first():
            raise HTTPException(status_code=400, detail="Это имя пользователя уже занято")

    user.username = username
    user.email = email
    user.bio = bio.strip() if bio else None

    _sync_interests(db, user, interest_ids)

    if avatar and avatar.filename:
        if user.avatar_url:
            remove_media_file(user.avatar_url)
        user.avatar_url = image_service.validate_and_save_image(avatar)

    db.commit()
    db.refresh(user)
    user = _load_profile_user(db, user.id)
    return user_to_detail_read(user)


@router.get("/comments", response_model=List[CommentHistoryRead])
def get_my_comments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
):
    comments = (
        db.query(Comment)
        .options(joinedload(Comment.post))
        .filter(Comment.user_id == current_user.id)
        .order_by(Comment.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [
        CommentHistoryRead(
            id=c.id,
            text=c.text,
            post_id=c.post_id,
            post_title=c.post.title if c.post else "Удалённая публикация",
            created_at=c.created_at,
        )
        for c in comments
    ]
