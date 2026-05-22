import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware  # Добавлено для интеграции с фронтендом

from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.posts import router as posts_router
from app.api.comments import router as comments_router
from app.api.profile import router as profile_router
from app.api.categories import router as categories_router
from app.api.admin import router as admin_router
from app.core.database import Base, engine

# Принудительно импортируем модели, чтобы Base.metadata знал о них при создании таблиц
from app.models.user import User
from app.models.tag import Tag
from app.models.like import Like

# Автоматическое создание таблиц в БД при запуске приложения
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Платформа для публикации творческих работ и модерирования контента."
)

# НАСТРОЙКА CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],\
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все типы запросов: GET, POST, PUT, PATCH, DELETE
    allow_headers=["*"],  # Разрешаем любые заголовки, включая Authorization для JWT
)

# НАСТРОЙКА ХРАНИЛИЩА МЕДИАФАЙЛОВ
# Динамически определяем абсолютный путь к папке media на сервере
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "media"))

if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

# Монтируем раздачу статических файлов (изображения постов, аватары) по адресу /media
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

# РЕГИСТРАЦИЯ РОУТЕРОВ (Реализация REST API архитектуры)
app.include_router(auth_router, prefix="/api")
app.include_router(posts_router, prefix="/api")
app.include_router(comments_router, prefix="/api")
app.include_router(profile_router, prefix="/api")
app.include_router(categories_router, prefix="/api")
app.include_router(admin_router, prefix="/api")


@app.get("/", tags=["Системные"])
def root():
    """Эндпоинт проверки работоспособности сервиса (Health Check)."""
    return {"status": "healthy", "message": "Creative Network API is running"}