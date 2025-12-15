from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.copy import Copy
from app.models.book import Book

def get_copy(db: Session, copy_id: int) -> Optional[Copy]:
    return db.query(Copy).filter(Copy.id == copy_id).first()

def get_copy_by_inventory(db: Session, inventory_number: str) -> Optional[Copy]:
    return db.query(Copy).filter(Copy.inventory_number == inventory_number).first()

def get_copies(db: Session, skip: int = 0, limit: int = 100) -> List[Copy]:
    return db.query(Copy).offset(skip).limit(limit).all()

def get_available_copies(db: Session, book_id: int) -> List[Copy]:
    """Получить доступные экземпляры книги"""
    return db.query(Copy).filter(
        Copy.book_id == book_id,
        Copy.status == "available"
    ).all()

def create_copy(db: Session, copy_data: dict) -> Copy:
    db_copy = Copy(**copy_data)
    db.add(db_copy)
    db.commit()
    db.refresh(db_copy)
    return db_copy

def update_copy(db: Session, copy_id: int, copy_data: dict) -> Optional[Copy]:
    db_copy = get_copy(db, copy_id)
    if not db_copy:
        return None
    
    for field, value in copy_data.items():
        if value is not None:
            setattr(db_copy, field, value)
    
    db.commit()
    db.refresh(db_copy)
    return db_copy

def delete_copy(db: Session, copy_id: int) -> bool:
    db_copy = get_copy(db, copy_id)
    if not db_copy:
        return False
    
    db.delete(db_copy)
    db.commit()
    return True

def get_copies_with_books(db: Session, skip: int = 0, limit: int = 100) -> List[Copy]:
    """Получить экземпляры с информацией о книгах"""
    return db.query(Copy).join(Book).offset(skip).limit(limit).all()