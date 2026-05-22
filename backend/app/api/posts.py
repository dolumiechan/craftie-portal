import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.post import Post, PostImage
from app.models.tag import Tag
from app.schemas.post import PostRead, PostDetailRead, PostUpdate

router = APIRouter(prefix="/posts", tags=["Посты и Публикации"])

# Папка, куда физически будут сохраняться картинки постов
UPLOAD_DIR = "media"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=List[PostRead])
def list_posts(
    category_id: Optional[int] = None, 
    db: Session = Depends(get_db), 
    skip: int = 0, 
    limit: int = 10
):
    """
    Получение списка постов (Лента публикаций).
    Поддерживает фильтрацию по ID категории.
    """
    query = db.query(Post)
    
    # Если фронтенд передал конкретную категорию - фильтруем по ней
    if category_id is not None:
        query = query.filter(Post.category_id == category_id)
        
    # Сортируем посты от новых к старым и отдаем порциями (пагинация)
    return query.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()

@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    tags_json: Optional[str] = Form(None),  # Получаем теги в виде JSON-строки, например: '["арт", "хобби"]'
    file: UploadFile = File(...),           # Файл изображения
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Создание новой публикации с загрузкой картинки и привязкой тегов
    """
    # 1. Валидация файла изображения
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Разрешено загружать только изображения")

    # Генерируем уникальное имя для файла, чтобы они не перезаписывали друг друга
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Сохраняем файл на диск сервера
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # URL, по которому фронтенд сможет открыть эту картинку
    image_url = f"/media/{unique_filename}"

    # 2. Создаем сам пост
    new_post = Post(
        title=title,
        description=description,
        category_id=category_id,
        author_id=current_user.id
    )

    # 3. Обрабатываем теги, если они переданы
    if tags_json:
        try:
            tag_names = json.loads(tags_json)
            for name in tag_names:
                name_stripped = name.strip().lower()
                if name_stripped:
                    # Ищем тег в базе, если его нет - создаем новый
                    tag = db.query(Tag).filter(Tag.name == name_stripped).first()
                    if not tag:
                        tag = Tag(name=name_stripped)
                        db.add(tag)
                    new_post.tags.append(tag)
        except Exception:
            raise HTTPException(status_code=400, detail="Неверный формат поля tags_json")

    db.add(new_post)
    db.flush()  # Получаем ID созданного поста перед коммитом

    # 4. Сохраняем ссылку на картинку в таблицу post_images
    post_image = PostImage(post_id=new_post.id, image_url=image_url)
    db.add(post_image)

    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=PostDetailRead)
def get_post(id: int, db: Session = Depends(get_db)):
    """Получение полной информации об одном посте по его ID."""
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    return post


@router.put("/{id}", response_model=PostRead)
def update_post(
    id: int, 
    post_update: PostUpdate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Редактирование текстовых полей поста его автором."""
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
    """Удаление поста. Доступно автору или администрации."""
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    
    is_author = post.author_id == current_user.id
    is_staff = current_user.role and current_user.role.name in ["moderator", "admin"]
    
    if not is_author and not is_staff:
        raise HTTPException(
            status_code=403, 
            detail="Нет прав на удаление этого поста. Вы должны быть автором или администратором."
        )
        
    db.delete(post)
    db.commit()
    return None