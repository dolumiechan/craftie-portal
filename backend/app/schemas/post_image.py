from pydantic import BaseModel, ConfigDict

class PostImageBase(BaseModel):
    image_url: str

class PostImageCreate(PostImageBase):
    post_id: int

class PostImageRead(PostImageBase):
    id: int
    post_id: int

    model_config = ConfigDict(from_attributes=True)