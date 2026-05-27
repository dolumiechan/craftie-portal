"""Сборка данных ленты публикаций для API."""

import os
from typing import Dict, Iterable, List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.core.image_service import UPLOAD_DIR
from app.models.comment import Comment
from app.models.post import Post
from app.schemas.post import PostDetailRead, PostFeedRead

POST_LOAD_OPTIONS = (
    joinedload(Post.author),
    joinedload(Post.category),
    joinedload(Post.images),
)

POST_DETAIL_OPTIONS = (
    *POST_LOAD_OPTIONS,
    joinedload(Post.tags),
)


def remove_media_file(image_url: Optional[str]) -> None:
    if not image_url:
        return
    path = image_url.lstrip("/")
    if path.startswith(UPLOAD_DIR) and os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass


def get_comment_counts(db: Session, post_ids: Iterable[int]) -> Dict[int, int]:
    ids = list(post_ids)
    if not ids:
        return {}
    rows = (
        db.query(Comment.post_id, func.count(Comment.id))
        .filter(Comment.post_id.in_(ids))
        .group_by(Comment.post_id)
        .all()
    )
    return {post_id: count for post_id, count in rows}


def post_to_feed_read(post: Post, comments_count: int = 0) -> PostFeedRead:
    image_url = post.images[0].image_url if post.images else None
    return PostFeedRead(
        id=post.id,
        title=post.title,
        description=post.description,
        author_id=post.author_id,
        author_username=post.author.username if post.author else "Автор",
        category_id=post.category_id,
        category_name=post.category.name if post.category else None,
        created_at=post.created_at,
        image_url=image_url,
        comments_count=comments_count,
        is_hidden=bool(post.is_hidden),
    )


def posts_to_feed_reads(db: Session, posts: List[Post]) -> List[PostFeedRead]:
    counts = get_comment_counts(db, [p.id for p in posts])
    return [post_to_feed_read(p, counts.get(p.id, 0)) for p in posts]


def post_to_detail_read(post: Post, comments_count: int = 0) -> PostDetailRead:
    return PostDetailRead(
        id=post.id,
        title=post.title,
        description=post.description,
        category_id=post.category_id,
        author_id=post.author_id,
        created_at=post.created_at,
        author_username=post.author.username if post.author else "Автор",
        category_name=post.category.name if post.category else None,
        image_url=post.images[0].image_url if post.images else None,
        comments_count=comments_count,
        category=post.category,
        images=post.images,
        tags=list(post.tags) if post.tags else [],
    )
