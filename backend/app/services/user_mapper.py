from app.models.user import User
from app.schemas.user import UserMeRead, UserDetailRead


def user_to_me_read(user: User) -> UserMeRead:
    return UserMeRead(
        id=user.id,
        email=user.email,
        username=user.username,
        role_id=user.role_id,
        created_at=user.created_at,
        role_name=user.role.name if user.role else None,
        is_active=user.is_active,
        bio=user.bio,
        avatar_url=user.avatar_url,
    )


def user_to_detail_read(user: User) -> UserDetailRead:
    return UserDetailRead(
        id=user.id,
        email=user.email,
        username=user.username,
        role_id=user.role_id,
        created_at=user.created_at,
        role_name=user.role.name if user.role else None,
        bio=user.bio,
        avatar_url=user.avatar_url,
        interests=list(user.interests) if user.interests else [],
        posts=list(user.posts) if user.posts else [],
    )
