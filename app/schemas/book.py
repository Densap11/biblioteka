from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Базовая схема книги
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Название книги")
    author: str = Field(..., min_length=1, max_length=255, description="Автор книги")
    year: Optional[int] = Field(None, ge=1000, le=2100, description="Год издания")
    publisher: Optional[str] = Field(None, max_length=255, description="Издательство")
    genre: Optional[str] = Field(None, max_length=100, description="Жанр")
    isbn: Optional[str] = Field(None, max_length=20, description="ISBN")

# Схема для создания книги
class BookCreate(BookBase):
    pass

# Схема для обновления книги
class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    year: Optional[int] = Field(None, ge=1000, le=2100)
    publisher: Optional[str] = Field(None, max_length=255)
    genre: Optional[str] = Field(None, max_length=100)
    isbn: Optional[str] = Field(None, max_length=20)

# Схема книги из БД (с id и датами)
class BookInDB(BookBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Ранее orm_mode в Pydantic v2