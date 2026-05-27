from pydantic import BaseModel, ConfigDict

class InterestCategoryBase(BaseModel):
    """ Базовая схема для категории интересов. Содержит общие поля. """
    name: str

class InterestCategoryCreate(InterestCategoryBase):
    """ Схема для создания новой категории. """
    pass


class InterestCategoryUpdate(InterestCategoryBase):
    """ Схема для обновления категории. """
    pass

class InterestCategoryRead(InterestCategoryBase):
    """ Схема для отправки данных о категории клиенту. Добавляет системный ID. """
    id: int

    # Настройка позволяет Pydantic автоматически читать данные из ORM-моделей SQLAlchemy
    model_config = ConfigDict(from_attributes=True)