import csv
import io
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.core.permissions import verify_admin, verify_staff
from app.models.user import User
from app.models.user_log import UserLog
from app.models.post import Post
from app.schemas.user import UserRoleUpdate
from app.schemas.admin import AdminUserRead, AdminLogRead, AdminPostListResponse
from app.services.logger import log_user_action as log_action
from app.services.post_feed import posts_to_feed_reads
from app.services.post_feed import POST_LOAD_OPTIONS, remove_media_file

router = APIRouter(prefix="/admin", tags=["Администрирование и Модерация"])


def _user_to_admin_read(user: User) -> AdminUserRead:
    return AdminUserRead(
        id=user.id,
        username=user.username,
        email=user.email,
        role_name=user.role.name if user.role else None,
        is_active=user.is_active,
        created_at=user.created_at,
    )


@router.get("/users", response_model=List[AdminUserRead])
def list_users(db: Session = Depends(get_db), admin: User = Depends(verify_admin)):
    users = db.query(User).options(joinedload(User.role)).order_by(User.id).all()
    return [_user_to_admin_read(u) for u in users]


@router.patch("/users/{user_id}/role")
def assign_user_role(
    user_id: int,
    body: UserRoleUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(verify_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if user.id == admin.id and body.role != "admin":
        raise HTTPException(status_code=400, detail="Нельзя снять роль admin с самого себя")

    from app.models.user import Role

    role = db.query(Role).filter(Role.name == body.role).first()
    if not role:
        raise HTTPException(status_code=400, detail="Роль не найдена")

    old_role = user.role.name if user.role else "none"
    user.role_id = role.id
    db.commit()
    log_action(db, user_id=admin.id, action="ASSIGN_ROLE", details=f"user_id={user.id} {old_role}->{body.role}")
    return {"message": f"Роль обновлена на «{body.role}»"}


@router.patch("/users/{user_id}/toggle-status")
def toggle_user_status(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(verify_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Нельзя заблокировать себя")

    user.is_active = not user.is_active
    db.commit()
    status_text = "BLOCKED" if not user.is_active else "UNBLOCKED"
    log_action(db, user_id=admin.id, action=status_text, details=f"user_id={user.id}")
    return {"message": f"Активен: {user.is_active}"}


@router.get("/logs", response_model=List[AdminLogRead])
def get_system_logs(db: Session = Depends(get_db), admin: User = Depends(verify_admin)):
    logs = (
        db.query(UserLog)
        .options(joinedload(UserLog.user))
        .order_by(UserLog.timestamp.desc())
        .limit(200)
        .all()
    )
    return [
        AdminLogRead(
            id=log.id,
            user_id=log.user_id,
            actor_username=log.user.username if log.user else None,
            action=log.action,
            details=log.details,
            timestamp=log.timestamp,
        )
        for log in logs
    ]


@router.get("/users/export/csv")
def export_users_to_csv(db: Session = Depends(get_db), admin: User = Depends(verify_admin)):
    users = db.query(User).options(joinedload(User.role)).all()
    output = io.StringIO()
    output.write("\ufeff")
    writer = csv.writer(output, delimiter=";")
    writer.writerow(["ID", "Имя пользователя", "Email", "Роль", "Статус активности"])
    for u in users:
        role_name = u.role.name if u.role else "Нет роли"
        status_active = "Активен" if u.is_active else "Заблокирован"
        writer.writerow([u.id, u.username, u.email, role_name, status_active])
    output.seek(0)
    log_action(db, user_id=admin.id, action="EXPORT_CSV", details="users export")
    return StreamingResponse(
        iter([output.getvalue().encode("utf-8")]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=users_export.csv"},
    )


@router.get("/posts", response_model=AdminPostListResponse)
def list_all_posts(
    db: Session = Depends(get_db),
    staff: User = Depends(verify_staff),
    skip: int = 0,
    limit: int = 50,
):
    query = db.query(Post)
    total = query.count()
    posts = (
        query.options(*POST_LOAD_OPTIONS)
        .order_by(Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return AdminPostListResponse(items=posts_to_feed_reads(db, posts), total=total)


@router.patch("/posts/{post_id}/toggle-hidden")
def toggle_post_hidden(
    post_id: int,
    db: Session = Depends(get_db),
    staff: User = Depends(verify_staff),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Публикация не найдена")

    post.is_hidden = not post.is_hidden
    db.commit()
    action = "HIDE_POST" if post.is_hidden else "UNHIDE_POST"
    log_action(db, user_id=staff.id, action=action, details=f"post_id={post.id}")
    return {"message": "Скрыта" if post.is_hidden else "Видна", "is_hidden": post.is_hidden}


@router.delete("/posts/{post_id}", status_code=204)
def admin_delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    staff: User = Depends(verify_staff),
):
    post = db.query(Post).options(joinedload(Post.images)).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Публикация не найдена")

    for img in post.images:
        remove_media_file(img.image_url)

    log_action(db, user_id=staff.id, action="ADMIN_DELETE_POST", details=f"post_id={post.id}")
    db.delete(post)
    db.commit()
    return None
