import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# Тестовая база данных в памяти
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Фикстура для сессии БД
@pytest.fixture(scope="function")
def db_session():
    """Создает новую сессию БД для каждого теста"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# Фикстура для тестового клиента
@pytest.fixture(scope="function")
def client(db_session):
    """Создает тестовый клиент FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

# Фикстура для тестовых данных
@pytest.fixture(scope="function")
def test_book_data():
    return {
        "title": "Тестовая книга",
        "author": "Тестовый автор",
        "year": 2024,
        "publisher": "Тестовое издательство",
        "genre": "Тест",
        "isbn": "978-5-999-99999-9"
    }

@pytest.fixture(scope="function")
def test_reader_data():
    return {
        "full_name": "Тестовый Читатель",
        "library_card": "TEST-001",
        "email": "test@example.com",
        "phone": "+79990000000"
    }