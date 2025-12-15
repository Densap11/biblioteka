from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Book(Base):
    """Модель книги"""
    
    __tablename__ = "books"
    
    # Основные поля
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False, index=True)
    year = Column(Integer)
    publisher = Column(String(255))
    genre = Column(String(100))
    isbn = Column(String(20), unique=True, index=True)
    
    # Методанные
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"
    
    def to_dict(self):
        """Преобразование объекта в словарь"""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "publisher": self.publisher,
            "genre": self.genre,
            "isbn": self.isbn,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }