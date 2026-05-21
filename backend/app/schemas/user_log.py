<<<<<<< HEAD
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserLogBase(BaseModel):
    action: str

class UserLogRead(UserLogBase):
    id: int
    user_id: int
    timestamp: datetime

=======
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserLogBase(BaseModel):
    action: str

class UserLogRead(UserLogBase):
    id: int
    user_id: int
    timestamp: datetime

>>>>>>> 8d6cb81 (Add posts filtering/search with pagination and implement admin endpoints)
    model_config = ConfigDict(from_attributes=True)