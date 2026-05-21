<<<<<<< HEAD
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from app.schemas.post import PostRead

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    role_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserDetailRead(UserRead):
    posts: list[PostRead] = []

=======
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from app.schemas.post import PostRead

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    role_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserDetailRead(UserRead):
    posts: list[PostRead] = []

>>>>>>> 8d6cb81 (Add posts filtering/search with pagination and implement admin endpoints)
    model_config = ConfigDict(from_attributes=True)