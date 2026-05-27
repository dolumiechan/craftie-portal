import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.posts import router as posts_router
from app.api.comments import router as comments_router
from app.api.profile import router as profile_router
from app.api.categories import router as categories_router
from app.api.admin import router as admin_router
from app.api.likes import router as likes_router
from app.core.database import Base, engine, SessionLocal
from app.models.seeder import seed_data

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    seed_data(db)
finally:
    db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Платформа для публикации творческих работ и модерирования контента."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],\
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# НАСТРОЙКА ХРАНИЛИЩА МЕДИАФАЙЛОВ
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "media"))

if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

app.include_router(auth_router, prefix="/api")
app.include_router(posts_router, prefix="/api")
app.include_router(comments_router, prefix="/api")
app.include_router(profile_router, prefix="/api")
app.include_router(categories_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(likes_router, prefix="/api")


@app.get("/", tags=["Системные"])
def root():
    """Эндпоинт проверки работоспособности сервиса (Health Check)."""
    return {"status": "healthy", "message": "Creative Network API is running"}