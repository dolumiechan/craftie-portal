from pydantic import BaseModel, ConfigDict

class InterestCategoryBase(BaseModel):
    name: str

class InterestCategoryCreate(InterestCategoryBase):
    pass

class InterestCategoryRead(InterestCategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)