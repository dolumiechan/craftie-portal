import sys
import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User, Role
import bcrypt

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def create_super_user():
    db: Session = SessionLocal()
    try:
        roles_list = ["user", "moderator", "admin"]
        role_objects = {}
        for role_name in roles_list:
            role = db.query(Role).filter(Role.name == role_name).first()
            if not role:
                role = Role(name=role_name)
                db.add(role)
                db.commit()
                db.refresh(role)
            role_objects[role_name] = role

        admin_email = "admin@example.com"
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        
        if not existing_admin:
            password_hash = hash_password("admin123")
            
            new_admin = User(
                username="admin",
                email=admin_email,
                password_hash=password_hash,
                role_id=role_objects["admin"].id
            )
            db.add(new_admin)
            db.commit()
            print(f"Администратор {admin_email} успешно создан!")
        else:
            print(f"Администратор {admin_email} уже существует.")

    except Exception as e:
        db.rollback()
        print(f"Ошибка при создании админа: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_super_user()