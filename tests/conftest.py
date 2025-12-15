# tests/conftest.py - фикстуры для тестов
import pytest
import os
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base

# Используем временную базу данных в памяти для тестов
@pytest.fixture(scope="function")
def test_db():
    """Создает временную базу данных для каждого теста"""
    # Используем временную файл-базу чтобы избежать проблем с потоками при TestClient
    import tempfile
    tmp = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    db_path = tmp.name
    tmp.close()

    engine = create_engine(f'sqlite:///{db_path}', connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        try:
            os.unlink(db_path)
        except Exception:
            pass


# Тестовый клиент FastAPI, переопределяющий зависимость get_db
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db

@pytest.fixture(scope="function")
def client(test_db, monkeypatch):
    """Возвращает TestClient с переопределенной БД"""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.pop(get_db, None)


# Примеры данных для тестов
@pytest.fixture(scope="function")
def test_book_data():
    return {
        "title": "Тестовая книга",
        "author": "Тестовый автор",
        "year": 2024,
        "genre": "Тест"
    }


@pytest.fixture(scope="function")
def test_reader_data():
    return {
        "full_name": "Тестовый читатель",
        "library_card": "CARD-001",
        "email": "reader@example.test"
    }