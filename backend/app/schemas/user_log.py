from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserLogBase(BaseModel):
    """ Базовая схема логов. Фиксирует само действие. """
    action: str

class UserLogRead(UserLogBase):
    """ Схема для отображения логов в админ-панели. Добавляет автора и время события. """
    id: int
    user_id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)