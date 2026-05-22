from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Role(Base):
    """
    Таблица ролей пользователей (Администратор, пользователь).
    Нужна для разграничения прав доступа в системе.
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # Например: 'admin' или 'user'

    # Связь с пользователями (у одной роли может быть много пользователей)
    users = relationship("User", back_populates="role")

class User(Base):
    """
    Таблица пользователей.
    Хранит личные данные, хэш пароля и статус активности аккаунта.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)  # Храним защищенный хэш, а не чистый пароль
    
    # Внешний ключ на таблицу ролей. Если роль удалится, у пользователя просто сотрется связь (SET NULL)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
    
    # Дата регистрации, создается автоматически базой данных при создании записи
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Статус пользователя: True - активен, False - заблокирован (для модерации)
    is_active = Column(Boolean, default=True, nullable=False)

    # === Связи с другими таблицами (relationships) ===
    role = relationship("Role", back_populates="users")
    
    # Если пользователь удаляется, каскадно удаляем все связанные с ним данные
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    logs = relationship("UserLog", back_populates="user", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")