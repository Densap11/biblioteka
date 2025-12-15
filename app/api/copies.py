from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.database import get_db
from app.models.copy import Copy
from app.models.book import Book
from app.schemas.copy import CopyCreate, CopyInDB, CopyUpdate

router = APIRouter()

@router.get("/", response_model=List[CopyInDB])
def read_copies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: str = Query(None, description="Фильтр по статусу"),
    db: Session = Depends(get_db)
):
    """Получить список всех экземпляров"""
    query = db.query(Copy)
    
    if status:
        query = query.filter(Copy.status == status)
    
    copies = query.offset(skip).limit(limit).all()
    
    # Добавляем название книги к каждому экземпляру
    result = []
    for copy in copies:
        copy_dict = copy.__dict__.copy()
        book = db.query(Book).filter(Book.id == copy.book_id).first()
        if book:
            copy_dict["book_title"] = book.title
        result.append(CopyInDB(**copy_dict))
    
    return result

@router.get("/{copy_id}", response_model=CopyInDB)
def read_copy(copy_id: int, db: Session = Depends(get_db)):
    """Получить экземпляр по ID"""
    copy = db.query(Copy).filter(Copy.id == copy_id).first()
    if copy is None:
        raise HTTPException(status_code=404, detail="Экземпляр не найден")
    
    # Добавляем название книги
    copy_dict = copy.__dict__.copy()
    book = db.query(Book).filter(Book.id == copy.book_id).first()
    if book:
        copy_dict["book_title"] = book.title
    
    return CopyInDB(**copy_dict)

@router.get("/book/{book_id}/available", response_model=List[CopyInDB])
def read_available_copies(book_id: int, db: Session = Depends(get_db)):
    """Получить доступные экземпляры книги"""
    copies = db.query(Copy).filter(
        Copy.book_id == book_id,
        Copy.status == "available"
    ).all()
    
    # Добавляем название книги
    result = []
    for copy in copies:
        copy_dict = copy.__dict__.copy()
        book = db.query(Book).filter(Book.id == copy.book_id).first()
        if book:
            copy_dict["book_title"] = book.title
        result.append(CopyInDB(**copy_dict))
    
    return result

@router.get("/inventory/{inventory_number}", response_model=CopyInDB)
def read_copy_by_inventory(inventory_number: str, db: Session = Depends(get_db)):
    """Получить экземпляр по инвентарному номеру"""
    copy = db.query(Copy).filter(Copy.inventory_number == inventory_number).first()
    if copy is None:
        raise HTTPException(status_code=404, detail="Экземпляр не найден")
    
    # Добавляем название книги
    copy_dict = copy.__dict__.copy()
    book = db.query(Book).filter(Book.id == copy.book_id).first()
    if book:
        copy_dict["book_title"] = book.title
    
    return CopyInDB(**copy_dict)

@router.post("/", response_model=CopyInDB, status_code=201)
def create_copy(copy: CopyCreate, db: Session = Depends(get_db)):
    """Создать новый экземпляр"""
    # Проверяем, существует ли книга
    book = db.query(Book).filter(Book.id == copy.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    # Проверяем, есть ли уже экземпляр с таким инвентарным номером
    existing = db.query(Copy).filter(Copy.inventory_number == copy.inventory_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Экземпляр с таким инвентарным номером уже существует")
    
    db_copy = Copy(
        book_id=copy.book_id,
        inventory_number=copy.inventory_number,
        status=copy.status,
        acquisition_date=date.today()
    )
    db.add(db_copy)
    db.commit()
    db.refresh(db_copy)
    
    # Добавляем название книги
    copy_dict = db_copy.__dict__.copy()
    copy_dict["book_title"] = book.title
    
    return CopyInDB(**copy_dict)

@router.put("/{copy_id}", response_model=CopyInDB)
def update_copy(
    copy_id: int, 
    copy_update: CopyUpdate, 
    db: Session = Depends(get_db)
):
    """Обновить экземпляр"""
    copy = db.query(Copy).filter(Copy.id == copy_id).first()
    if copy is None:
        raise HTTPException(status_code=404, detail="Экземпляр не найден")
    
    # Обновляем поля
    update_data = copy_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(copy, field, value)
    
    db.commit()
    db.refresh(copy)
    
    # Добавляем название книги
    copy_dict = copy.__dict__.copy()
    book = db.query(Book).filter(Book.id == copy.book_id).first()
    if book:
        copy_dict["book_title"] = book.title
    
    return CopyInDB(**copy_dict)

@router.delete("/{copy_id}", status_code=204)
def delete_copy(copy_id: int, db: Session = Depends(get_db)):
    """Удалить экземпляр"""
    copy = db.query(Copy).filter(Copy.id == copy_id).first()
    if copy is None:
        raise HTTPException(status_code=404, detail="Экземпляр не найден")
    
    db.delete(copy)
    db.commit()
    return None

@router.patch("/{copy_id}/mark-borrowed", response_model=CopyInDB)
def mark_copy_borrowed(copy_id: int, db: Session = Depends(get_db)):
    """Пометить экземпляр как выданный"""
    copy = db.query(Copy).filter(Copy.id == copy_id).first()
    if copy is None:
        raise HTTPException(status_code=404, detail="Экземпляр не найден")
    
    copy.status = "borrowed"
    db.commit()
    db.refresh(copy)
    
    # Добавляем название книги
    copy_dict = copy.__dict__.copy()
    book = db.query(Book).filter(Book.id == copy.book_id).first()
    if book:
        copy_dict["book_title"] = book.title
    
    return CopyInDB(**copy_dict)

@router.patch("/{copy_id}/mark-available", response_model=CopyInDB)
def mark_copy_available(copy_id: int, db: Session = Depends(get_db)):
    """Пометить экземпляр как доступный"""
    copy = db.query(Copy).filter(Copy.id == copy_id).first()
    if copy is None:
        raise HTTPException(status_code=404, detail="Экземпляр не найден")
    
    copy.status = "available"
    db.commit()
    db.refresh(copy)
    
    # Добавляем название книги
    copy_dict = copy.__dict__.copy()
    book = db.query(Book).filter(Book.id == copy.book_id).first()
    if book:
        copy_dict["book_title"] = book.title
    
    return CopyInDB(**copy_dict)