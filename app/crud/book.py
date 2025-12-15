from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate

def get_book(db: Session, book_id: int) -> Optional[Book]:
    """Получить книгу по ID"""
    return db.query(Book).filter(Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
    """Получить список книг"""
    return db.query(Book).offset(skip).limit(limit).all()

def create_book(db: Session, book: BookCreate) -> Book:
    """Создать новую книгу"""
    db_book = Book(
        title=book.title,
        author=book.author,
        year=book.year,
        publisher=book.publisher,
        genre=book.genre,
        isbn=book.isbn
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book_update: BookUpdate) -> Optional[Book]:
    """Обновить книгу"""
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    
    update_data = book_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int) -> bool:
    """Удалить книгу"""
    db_book = get_book(db, book_id)
    if not db_book:
        return False
    
    db.delete(db_book)
    db.commit()
    return True

def search_books(db: Session, query: str) -> List[Book]:
    """Поиск книг по названию или автору"""
    return db.query(Book).filter(
        (Book.title.ilike(f"%{query}%")) | 
        (Book.author.ilike(f"%{query}%"))
    ).all()