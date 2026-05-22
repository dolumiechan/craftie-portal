import csv
import io
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.user_log import UserLog
from app.services.logger import log_user_action as log_action

router = APIRouter(prefix="/admin", tags=["Администрирование и Модерация"])


def verify_admin(current_user: User = Depends(get_current_user)):
    """
    Зависимость для проверки прав.
    Проверяет, что к эндпоинту обращается именно администратор.
    """
    # Проверяем имя роли через объект связи
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен. Данное действие доступно только администраторам системы."
        )
    return current_user


@router.get("/users", dependencies=[Depends(verify_admin)])
def list_users(db: Session = Depends(get_db)):
    """Получение списка всех пользователей системы для панели управления."""
    return db.query(User).all()


@router.patch("/users/{user_id}/toggle-status")
def toggle_user_status(user_id: int, db: Session = Depends(get_db), admin: User = Depends(verify_admin)):
    """
    Блокировка и разблокировка пользователей.
    Позволяет временно закрыть доступ к платформе нарушителям правил.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Вы не можете заблокировать самого себя")

    # Меняем флаг активности на противоположный
    user.is_active = not user.is_active
    db.commit()

    # Фиксируем действие администратора в системный лог
    status_text = "BLOCKED" if not user.is_active else "UNBLOCKED"
    log_action(db, user_id=admin.id, action=status_text, details=f"Changed status for user_id={user.id}")

    return {"message": f"Статус пользователя успешно изменен. Активен: {user.is_active}"}


@router.get("/logs")
def get_system_logs(db: Session = Depends(get_db), admin: User = Depends(verify_admin)):
    """Просмотр истории действий (логов) для контроля работы модерации."""
    return db.query(UserLog).order_by(UserLog.timestamp.desc()).all()


@router.get("/users/export/csv")
def export_users_to_csv(db: Session = Depends(get_db), admin: User = Depends(verify_admin)):
    """
    Выгрузка списка пользователей в формате CSV.
    Файл оптимизирован для корректного открытия в Microsoft Excel на русском языке.
    """
    users = db.query(User).all()

    output = io.StringIO()
    
    # Добавляем BOM (\ufeff) в начало файла, чтобы Excel не ломал кириллицу
    output.write('\ufeff')
    
    writer = csv.writer(output, delimiter=';')
    
    # Заголовки таблицы
    writer.writerow(["ID", "Имя пользователя", "Email", "Роль", "Статус активности"])
    
    for u in users:
        # Извлекаем текстовое название роли, если она назначена
        role_name = u.role.name if u.role else "Нет роли"
        status_active = "Активен" if u.is_active else "Заблокирован"
        
        writer.writerow([u.id, u.username, u.email, role_name, status_active])
    
    output.seek(0)
    
    # Логируем выгрузку персональных данных
    log_action(db, user_id=admin.id, action="EXPORT_CSV", details="Exported users table to CSV")

    # Превращаем текст в байты UTF-8 для корректной передачи через сеть
    csv_bytes = output.getvalue().encode("utf-8")

    return StreamingResponse(
        iter([csv_bytes]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=users_export.csv",
            "Content-Type": "text/csv; charset=utf-8"
        }
    )