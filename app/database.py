from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Создаем движок базы данных
# Для SQLite нужно добавить connect_args для поддержки foreign keys
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}  # Только для SQLite
    )
else:
    engine = create_engine(settings.DATABASE_URL)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Зависимость для получения сессии БД
def get_db():
    """
    Функция для получения сессии базы данных.
    Используется в dependency injection FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()