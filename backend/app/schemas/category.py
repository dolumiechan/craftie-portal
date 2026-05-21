<<<<<<< HEAD
from pydantic import BaseModel, ConfigDict

class InterestCategoryBase(BaseModel):
    name: str

class InterestCategoryCreate(InterestCategoryBase):
    pass

class InterestCategoryRead(InterestCategoryBase):
    id: int

=======
from pydantic import BaseModel, ConfigDict

class InterestCategoryBase(BaseModel):
    name: str

class InterestCategoryCreate(InterestCategoryBase):
    pass

class InterestCategoryRead(InterestCategoryBase):
    id: int

>>>>>>> 8d6cb81 (Add posts filtering/search with pagination and implement admin endpoints)
    model_config = ConfigDict(from_attributes=True)