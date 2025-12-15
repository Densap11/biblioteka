import pytest
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate

def test_book_model_creation():
    """Тест создания модели книги"""
    book = Book(
        title="Тестовая книга",
        author="Тестовый автор",
        year=2024,
        publisher="Тест",
        genre="Тест",
        isbn="1234567890"
    )
    
    assert book.title == "Тестовая книга"
    assert book.author == "Тестовый автор"
    assert book.year == 2024
    assert book.publisher == "Тест"
    assert book.genre == "Тест"
    assert book.isbn == "1234567890"

def test_book_schema_validation():
    """Тест валидации схемы книги"""
    # Правильные данные
    book_data = {
        "title": "Книга",
        "author": "Автор",
        "year": 2024,
        "publisher": "Издательство",
        "genre": "Жанр",
        "isbn": "1234567890"
    }
    
    book = BookCreate(**book_data)
    assert book.title == "Книга"
    assert book.author == "Автор"
    
    # Неправильные данные (должны вызывать ошибку)
    with pytest.raises(ValueError):
        BookCreate(title="", author="Автор")  # Пустое название
    
    with pytest.raises(ValueError):
        BookCreate(title="Книга", author="", year=3000)  # Пустой автор, неверный год

def test_book_update_schema():
    """Тест схемы обновления книги"""
    # Частичное обновление
    update_data = {"title": "Новое название"}
    book_update = BookUpdate(**update_data)
    
    assert book_update.title == "Новое название"
    assert book_update.author is None
    
    # Полное обновление
    full_update = {
        "title": "Новое название",
        "author": "Новый автор",
        "year": 2025
    }
    book_update_full = BookUpdate(**full_update)
    
    assert book_update_full.title == "Новое название"
    assert book_update_full.author == "Новый автор"
    assert book_update_full.year == 2025

def test_book_to_dict_method():
    """Тест метода to_dict модели книги"""
    book = Book(
        id=1,
        title="Тестовая книга",
        author="Тестовый автор",
        year=2024
    )
    
    book_dict = book.to_dict()
    
    assert book_dict["id"] == 1
    assert book_dict["title"] == "Тестовая книга"
    assert book_dict["author"] == "Тестовый автор"
    assert book_dict["year"] == 2024
    assert "created_at" in book_dict