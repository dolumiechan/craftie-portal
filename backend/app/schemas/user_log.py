from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserLogBase(BaseModel):
    action: str

class UserLogRead(UserLogBase):
    id: int
    user_id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)