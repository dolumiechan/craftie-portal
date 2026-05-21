<<<<<<< HEAD
from pydantic import BaseModel, ConfigDict

class PostImageBase(BaseModel):
    image_url: str

class PostImageCreate(PostImageBase):
    post_id: int

class PostImageRead(PostImageBase):
    id: int
    post_id: int

=======
from pydantic import BaseModel, ConfigDict

class PostImageBase(BaseModel):
    image_url: str

class PostImageCreate(PostImageBase):
    post_id: int

class PostImageRead(PostImageBase):
    id: int
    post_id: int

>>>>>>> 8d6cb81 (Add posts filtering/search with pagination and implement admin endpoints)
    model_config = ConfigDict(from_attributes=True)