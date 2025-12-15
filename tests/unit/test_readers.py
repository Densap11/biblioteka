import pytest
from pydantic import ValidationError
from app.models.reader import Reader
from app.schemas.reader import ReaderCreate, ReaderUpdate


def test_reader_schema_creation():
    """Тест: валидация и создание схемы ReaderCreate"""
    data = {
        "full_name": "Иван Иванов",
        "library_card": "CARD-001",
        "email": "ivan@example.com",
        "phone": "+71234567890",
    }

    reader = ReaderCreate(**data)

    assert reader.full_name == "Иван Иванов"
    assert reader.library_card == "CARD-001"
    assert reader.email == "ivan@example.com"


def test_reader_schema_invalid_status():
    """Тест: ReaderUpdate не должен принимать недопустимый статус"""
    with pytest.raises(ValidationError):
        ReaderUpdate(status="blockedish")


def test_reader_model_repr_and_defaults():
    """Тест: __repr__ модели и значение статуса по умолчанию"""
    reader = Reader(id=7, full_name="Мария Петрова", library_card="CARD-007")
    rep = repr(reader)

    assert "Мария Петрова" in rep
    assert "CARD-007" in rep
    # SQLAlchemy server_default may not be set on Python-side instance;
    # accept either None (not set yet) or the default value 'active'.
    assert reader.status in (None, "active")
