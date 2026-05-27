from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.tag import post_tags

class Post(Base):
    """
    Таблица публикаций (постов пользователей).
    Содержит заголовок, описание, дату создания и внешние ключи автора и категории.
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("interest_categories.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_hidden = Column(Boolean, default=False, nullable=False)

    # === Отношения со связанными сущностями ===
    author = relationship("User", back_populates="posts")
    category = relationship("InterestCategory", back_populates="posts")
    images = relationship("PostImage", back_populates="post", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    
    # Связь многие-ко-многим с тегами через промежуточную таблицу post_tags
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")


class PostImage(Base):
    """
    Таблица для хранения путей к изображениям постов.
    Позволяет привязывать несколько картинок к одному посту (Один-ко-многим).
    """
    __tablename__ = "post_images"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(Text, nullable=False)  # Ссылка на файл на диске сервера

    post = relationship("Post", back_populates="images")