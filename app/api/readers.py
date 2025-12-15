from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.reader import Reader
from app.schemas.reader import ReaderCreate, ReaderInDB, ReaderUpdate

router = APIRouter()

@router.get("/", response_model=List[ReaderInDB])
def read_readers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Получить список всех читателей"""
    readers = db.query(Reader).offset(skip).limit(limit).all()
    return readers

@router.get("/{reader_id}", response_model=ReaderInDB)
def read_reader(reader_id: int, db: Session = Depends(get_db)):
    """Получить читателя по ID"""
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    return reader

@router.get("/card/{library_card}", response_model=ReaderInDB)
def read_reader_by_card(library_card: str, db: Session = Depends(get_db)):
    """Получить читателя по номеру читательского билета"""
    reader = db.query(Reader).filter(Reader.library_card == library_card).first()
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    return reader

@router.post("/", response_model=ReaderInDB, status_code=201)
def create_reader(reader: ReaderCreate, db: Session = Depends(get_db)):
    """Создать нового читателя"""
    # Проверяем, есть ли уже читатель с таким номером билета
    existing = db.query(Reader).filter(Reader.library_card == reader.library_card).first()
    if existing:
        raise HTTPException(status_code=400, detail="Читатель с таким номером билета уже существует")
    
    db_reader = Reader(
        full_name=reader.full_name,
        library_card=reader.library_card,
        email=reader.email,
        phone=reader.phone
    )
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader

@router.put("/{reader_id}", response_model=ReaderInDB)
def update_reader(
    reader_id: int, 
    reader_update: ReaderUpdate, 
    db: Session = Depends(get_db)
):
    """Обновить читателя"""
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    
    # Обновляем поля
    update_data = reader_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(reader, field, value)
    
    db.commit()
    db.refresh(reader)
    return reader

@router.delete("/{reader_id}", status_code=204)
def delete_reader(reader_id: int, db: Session = Depends(get_db)):
    """Удалить читателя"""
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    
    db.delete(reader)
    db.commit()
    return None

@router.patch("/{reader_id}/block", response_model=ReaderInDB)
def block_reader(reader_id: int, db: Session = Depends(get_db)):
    """Заблокировать читателя"""
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    
    reader.status = "blocked"
    db.commit()
    db.refresh(reader)
    return reader

@router.patch("/{reader_id}/activate", response_model=ReaderInDB)
def activate_reader(reader_id: int, db: Session = Depends(get_db)):
    """Активировать читателя"""
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    
    reader.status = "active"
    db.commit()
    db.refresh(reader)
    return reader