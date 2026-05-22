import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from PIL import Image as PILImage, ImageOps
import io

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import UserDetailRead

router = APIRouter(prefix="/profile", tags=["Личный кабинет автора"])

# Единая папка для хранения медиафайлов
UPLOAD_DIR = "media"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/", response_model=UserDetailRead)
def get_profile(current_user: User = Depends(get_current_user)):
    """
    Получение профиля текущего авторизованного автора
    Возвращает расширенные данные, включая биографию, аватар и интересы.
    """
    return current_user


@router.put("/", response_model=UserDetailRead)
def update_profile(
    username: str = Form(...),
    email: str = Form(...),
    bio: str = Form(None),
    avatar: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Редактирование профиля автора.
    
    Реализует:
    1. Проверку уникальности изменяемых email и username.
    2. Обновление текстовой информации о себе (био).
    3. Загрузку, валидацию через Pillow и оптимизацию аватара пользователя.
    """
    # Валидация уникальности email при его изменении
    if email != current_user.email:
        email_exists = db.query(User).filter(User.email == email).first()
        if email_exists:
            raise HTTPException(status_code=400, detail="Этот email уже зарегистрирован в системе")
            
    # Валидация уникальности username при его изменении
    if username != current_user.username:
        username_exists = db.query(User).filter(User.username == username).first()
        if username_exists:
            raise HTTPException(status_code=400, detail="Это имя пользователя уже занято")

    # Обновление базовых текстовых полей
    current_user.username = username
    current_user.email = email
    current_user.bio = bio

    # Обработка загрузки аватара
    if avatar:
        # Проверяем расширение файла на базовом уровне
        file_ext = os.path.splitext(avatar.filename)[1].lower()
        if file_ext not in [".jpg", ".jpeg", ".png"]:
            raise HTTPException(
                status_code=400, 
                detail="Недопустимый формат файла. Разрешены только JPG, JPEG и PNG."
            )

        try:
            # Читаем файл в память для обработки библиотекой Pillow
            contents = avatar.file.read()
            image = PILImage.open(io.BytesIO(contents))
            
            # Проверяем, что файл действительно является валидным изображением
            image.verify()
            
            # Переоткрываем для физического изменения (после verify() файл закрывается)
            image = PILImage.open(io.BytesIO(contents))
            
            # Автоматический ресайз аватара до 300x300 (квадрат)
            # чтобы пользователи не загружали огромные картинки весом по 20 МБ
            image = ImageOps.fit(image, (300, 300), PILImage.Resampling.LANCZOS)

            # Генерируем уникальное имя файла, чтобы избежать конфликтов
            unique_filename = f"avatar_{uuid.uuid4().hex}{file_ext}"
            file_path = os.path.join(UPLOAD_DIR, unique_filename)

            # Сохраняем оптимизированное изображение на сервер в папку media
            image.save(file_path)
            
            # Удаляем старый файл аватара, если он существовал, чтобы не забивать диск
            if current_user.avatar_url:
                old_path = current_user.avatar_url.lstrip("/")
                if os.path.exists(old_path) and old_path.startswith(UPLOAD_DIR):
                    try:
                        os.remove(old_path)
                    except Exception:
                        pass # Если файл не нашелся или заблокирован, просто идем дальше

            # Записываем относительный веб-путь к аватару в БД
            current_user.avatar_url = f"/media/{unique_filename}"

        except Exception as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Ошибка при обработке изображения библиотекой Pillow: {str(e)}"
            )

    db.commit()
    db.refresh(current_user)
    return current_user