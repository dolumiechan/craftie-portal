from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import UserDetailRead, UserCreate

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/", response_model=UserDetailRead)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/", response_model=UserDetailRead)
def update_profile(username: str, email: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if email != current_user.email and db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email уже занят")
    if username != current_user.username and db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username уже занят")
        
    current_user.username = username
    current_user.email = email
    db.commit()
    db.refresh(current_user)
    return current_user