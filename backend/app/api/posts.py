import json
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.core.image_service import image_service
from app.core.security import get_current_user, get_current_user_optional
from app.core.permissions import is_staff_user
from app.models.user import User
from app.models.post import Post, PostImage
from app.models.tag import Tag
from app.schemas.post import PostDetailRead, PostFeedListResponse, PostFeedRead
from app.services.post_feed import (
    posts_to_feed_reads,
    post_to_detail_read,
    get_comment_counts,
    POST_LOAD_OPTIONS,
    POST_DETAIL_OPTIONS,
    remove_media_file,
)
from app.services.logger import log_user_action

router = APIRouter(prefix="/posts", tags=["Посты и Публикации"])

def _apply_feed_filters(query, category_id: Optional[int], search: Optional[str]):
    if category_id is not None:
        query = query.filter(Post.category_id == category_id)
    if search and search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Post.title.ilike(term),
                Post.description.ilike(term),
            )
        )
    return query


def _apply_tags(db: Session, post: Post, tags_json: Optional[str]) -> None:
    if tags_json is None:
        return
    try:
        tag_names = json.loads(tags_json)
        if not isinstance(tag_names, list):
            raise ValueError("tags_json must be a list")
    except (json.JSONDecodeError, ValueError):
        raise HTTPException(status_code=400, detail="Неверный формат tags_json")

    post.tags.clear()
    for name in tag_names:
        name_stripped = str(name).strip().lower()
        if not name_stripped:
            continue
        tag = db.query(Tag).filter(Tag.name == name_stripped).first()
        if not tag:
            tag = Tag(name=name_stripped)
            db.add(tag)
        post.tags.append(tag)


@router.get("/", response_model=PostFeedListResponse)
def list_posts(
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
):
    filtered = _apply_feed_filters(db.query(Post), category_id, search).filter(
        Post.is_hidden.is_(False)
    )
    total = filtered.count()
    posts = (
        filtered.options(*POST_LOAD_OPTIONS)
        .order_by(Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return PostFeedListResponse(
        items=posts_to_feed_reads(db, posts),
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/my", response_model=List[PostFeedRead])
def list_my_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 50,
):
    posts = (
        db.query(Post)
        .filter(Post.author_id == current_user.id)
        .options(*POST_LOAD_OPTIONS)
        .order_by(Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return posts_to_feed_reads(db, posts)


@router.post("/", response_model=PostDetailRead, status_code=status.HTTP_201_CREATED)
def create_post(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    tags_json: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    image_url = image_service.validate_and_save_image(file)

    new_post = Post(
        title=title,
        description=description,
        category_id=category_id,
        author_id=current_user.id,
    )
    db.add(new_post)
    db.flush()

    _apply_tags(db, new_post, tags_json or "[]")
    db.add(PostImage(post_id=new_post.id, image_url=image_url))

    log_user_action(
        db,
        user_id=current_user.id,
        action="CREATE_POST",
        details=f"post_id={new_post.id}",
    )

    db.commit()
    post = (
        db.query(Post)
        .options(*POST_DETAIL_OPTIONS)
        .filter(Post.id == new_post.id)
        .first()
    )
    return post_to_detail_read(post, 0)


@router.get("/{id}", response_model=PostDetailRead)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    post = (
        db.query(Post)
        .options(*POST_DETAIL_OPTIONS)
        .filter(Post.id == id)
        .first()
    )
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    if post.is_hidden and (not current_user or not is_staff_user(current_user)):
        raise HTTPException(status_code=404, detail="Пост не найден")
    counts = get_comment_counts(db, [post.id])
    return post_to_detail_read(post, counts.get(post.id, 0))


@router.put("/{id}", response_model=PostDetailRead)
def update_post(
    id: int,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    tags_json: Optional[str] = Form(None),
    file: UploadFile = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = (
        db.query(Post)
        .options(joinedload(Post.images), joinedload(Post.tags))
        .filter(Post.id == id)
        .first()
    )
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав на редактирование этого поста")

    post.title = title
    post.description = description
    post.category_id = category_id
    _apply_tags(db, post, tags_json)

    if file and file.filename:
        image_url = image_service.validate_and_save_image(file)
        if post.images:
            remove_media_file(post.images[0].image_url)
            post.images[0].image_url = image_url
        else:
            db.add(PostImage(post_id=post.id, image_url=image_url))

    log_user_action(
        db,
        user_id=current_user.id,
        action="UPDATE_POST",
        details=f"post_id={post.id}",
    )

    db.commit()
    post = (
        db.query(Post)
        .options(*POST_DETAIL_OPTIONS)
        .filter(Post.id == id)
        .first()
    )
    counts = get_comment_counts(db, [post.id])
    return post_to_detail_read(post, counts.get(post.id, 0))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = (
        db.query(Post)
        .options(joinedload(Post.images))
        .filter(Post.id == id)
        .first()
    )
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    is_author = post.author_id == current_user.id
    is_staff = current_user.role and current_user.role.name in ["moderator", "admin"]

    if not is_author and not is_staff:
        raise HTTPException(
            status_code=403,
            detail="Нет прав на удаление этого поста.",
        )

    for img in post.images:
        remove_media_file(img.image_url)

    log_user_action(
        db,
        user_id=current_user.id,
        action="DELETE_POST",
        details=f"post_id={post.id}",
    )

    db.delete(post)
    db.commit()
    return None
