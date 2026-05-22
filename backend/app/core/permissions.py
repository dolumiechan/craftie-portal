from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user
from app.models.user import User

class RoleChecker:
    """
    Класс для проверки ролей пользователей.
    
    Помогает быстро закрывать разные эндпоинты от обычных пользователей.
    При создании принимает список разрешенных ролей, например: ["admin", "moderator"].
    """
    def __init__(self, allowed_roles: list[str]):
        # Сохраняем список ролей, которым разрешен доступ
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        """
        Метод срабатывает автоматически, когда мы передаем класс в Depends().
        Он проверяет, есть ли у текущего пользователя нужные права.
        """
        # Проверяем, привязана ли вообще какая-то роль к пользователю
        if not current_user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="У вас нет назначенной роли в системе"
            )
        
        # Проверяем, входит ли имя роли пользователя в список разрешенных
        if current_user.role.name not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Доступ запрещен. Требуются права: {', '.join(self.allowed_roles)}"
            )
            
        # Если всё хорошо, возвращаем пользователя дальше в эндпоинт
        return current_user