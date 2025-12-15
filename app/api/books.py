from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import crud
from app.schemas.book import BookCreate, BookUpdate, BookInDB

router = APIRouter()

@router.get("/", response_model=List[BookInDB])
def read_books(
    skip: int = Query(0, ge=0, description="Пропустить первых N записей"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    db: Session = Depends(get_db)
):
    """Получить список всех книг"""
    books = crud.book.get_books(db, skip=skip, limit=limit)
    return books

@router.get("/{book_id}", response_model=BookInDB)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Получить книгу по ID"""
    db_book = crud.book.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return db_book

@router.post("/", response_model=BookInDB, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Создать новую книгу"""
    return crud.book.create_book(db=db, book=book)

@router.put("/{book_id}", response_model=BookInDB)
def update_book(
    book_id: int, 
    book_update: BookUpdate, 
    db: Session = Depends(get_db)
):
    """Обновить книгу"""
    db_book = crud.book.update_book(db, book_id=book_id, book_update=book_update)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return db_book

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удалить книгу"""
    success = crud.book.delete_book(db, book_id=book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return None

@router.get("/search/", response_model=List[BookInDB])
def search_books(
    q: str = Query(..., min_length=1, description="Поисковый запрос"),
    db: Session = Depends(get_db)
):
    """Поиск книг по названию или автору"""
    books = crud.book.search_books(db, query=q)
    if not books:
        raise HTTPException(status_code=404, detail="Книги не найдены")
    return books