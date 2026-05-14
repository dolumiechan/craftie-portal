from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user
from app.models.user import User

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        """
        Принимает список ролей, которым разрешен доступ.
        Пример: allowed_roles=["admin", "moderator"]
        """
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if not current_user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="У вас нет назначенной роли в системе"
            )
        
        if current_user.role.name not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Доступ запрещен. Требуются права: {', '.join(self.allowed_roles)}"
            )
            
        return current_user