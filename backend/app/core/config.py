from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Класс конфигурации и валидации окружения среды.
    
    Использует библиотеку Pydantic v2 для строгого контроля типов переменных.
    Если в файле .env будет отсутствовать обязательная переменная или тип данных 
    не будет соответствовать объявленному (например, если порт будет строкой, 
    которую нельзя привести к int), приложение выбросит ошибку ValidationError 
    еще на этапе запуска контейнера, предотвращая работу в неопределенном состоянии.
    """
    
    PROJECT_NAME: str = "Craftie portal"
    SECRET_KEY: str = "super-secret-key-change-me-in-production"

    # НАСТРОЙКИ ПОДКЛЮЧЕНИЯ К СУБД POSTGRESQL
    # Данные свойства автоматически маппятся (сопоставляются) с одноименными переменными из .env
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    @property
    def DATABASE_URL(self) -> str:
        """
        Динамическое свойство для сборки строки подключения.
        
        Использует драйвер 'psycopg2' для синхронного взаимодействия SQLAlchemy с PostgreSQL.
        Позволяет изолированно и безопасно хранить учетные данные в .env и автоматически 
        формирует валидный URL для инициализации движка базы данных.
        """
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Настройка источника конфигурации
    # env_file=".env" указывает Pydantic автоматически считывать переменные из локального файла окружения
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Инициализируем синглтон настроек для импорта во все модули бэкенда
settings = Settings()