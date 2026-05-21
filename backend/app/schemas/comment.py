<<<<<<< HEAD
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    post_id: int

class CommentRead(CommentBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime

=======
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    post_id: int

class CommentRead(CommentBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime

>>>>>>> 8d6cb81 (Add posts filtering/search with pagination and implement admin endpoints)
    model_config = ConfigDict(from_attributes=True)