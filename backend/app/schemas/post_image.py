from pydantic import BaseModel, ConfigDict

class PostImageBase(BaseModel):
    """ Базовая схема для изображений к постам. """
    image_url: str

class PostImageCreate(PostImageBase):
    """ Схема для сохранения картинки. Связывает её с конкретным постом. """
    post_id: int

class PostImageRead(PostImageBase):
    """ Схема для отдачи данных об изображении фронтенду. """
    id: int
    post_id: int

    model_config = ConfigDict(from_attributes=True)