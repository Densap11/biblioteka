import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Загружаем переменные окружения
load_dotenv()

class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Настройки приложения
    APP_NAME: str = "Библиотечная система"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Настройки базы данных
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./library.db"  # По умолчанию SQLite
    )
    
    # Настройки безопасности
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Бизнес-правила
    MAX_BOOKS_PER_READER: int = 5
    LOAN_PERIOD_DAYS: int = 14
    EXTENSION_DAYS: int = 7
    FINE_PER_DAY: float = 10.0  # Штраф за день просрочки
    
    # Настройки API
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"

# Создаем экземпляр настроек
settings = Settings()