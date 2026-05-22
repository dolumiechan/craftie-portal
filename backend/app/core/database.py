from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.core.config import settings
from typing import Generator

# ИНИЦИАЛИЗАЦИЯ ДВИЖКА БАЗЫ ДАННЫХ (Engine)
# settings.DATABASE_URL подтягивает строку подключения из конфигурационного файла (.env)
# pool_pre_ping=True - важный параметр отказоустойчивости. Перед выполнением каждого запроса 
# он отправляет тестовый пинг в БД. Если соединение разорвано (например, перезапуск контейнера БД), 
# движок прозрачно пересоздаст его, предотвращая падение API с ошибкой 500.
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# ФАБРИКА СЕССИЙ (SessionLocal)
# Конфигурирует изолированные транзакции для каждого входящего HTTP-запроса.
# autocommit=False - запрещает автоматическую фиксацию изменений. Изменения сохраняются на диск 
# только при явном вызове db.commit().
# autoflush=False — отключает автоматический сброс изменений в память БД перед каждым запросом.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# БАЗОВЫЙ ДЕКЛАРАТИВНЫЙ КЛАСС (Base)
# От него будут наследоваться все ORM-модели проекта (User, Post, Comment и др.).
# Он сопоставляет свойства Python-классов со структурой таблиц в СУБД (PostgreSQL/SQLite).
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Функция-провайдер (Dependency Injection) для управления жизненным циклом сессии БД.
    
    Использует контекстный генератор (yield) для изоляции транзакций:
    1. Инициализирует чистое подключение из пула для нового HTTP-запроса.
    2. Передает управление эндпоинту бэкенда.
    3. Блок 'finally' гарантирует закрытие сессии и её возврат в пул подключений 
       сразу после завершения обработки запроса, предотвращая утечки памяти и лимитов СУБД.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()