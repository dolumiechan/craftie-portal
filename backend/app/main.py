import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import settings

from app.api.auth import router as auth_router
from app.api.posts import router as posts_router
from app.api.comments import router as comments_router
from app.api.profile import router as profile_router

app = FastAPI(title=settings.PROJECT_NAME)

MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "media")
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

app.include_router(auth_router, prefix="/api")
app.include_router(posts_router, prefix="/api")
app.include_router(comments_router, prefix="/api")
app.include_router(profile_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API is running"}