from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.reader import Reader

def get_reader(db: Session, reader_id: int) -> Optional[Reader]:
    return db.query(Reader).filter(Reader.id == reader_id).first()

def get_reader_by_card(db: Session, library_card: str) -> Optional[Reader]:
    return db.query(Reader).filter(Reader.library_card == library_card).first()

def get_readers(db: Session, skip: int = 0, limit: int = 100) -> List[Reader]:
    return db.query(Reader).offset(skip).limit(limit).all()

def create_reader(db: Session, reader_data: dict) -> Reader:
    db_reader = Reader(**reader_data)
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader

def update_reader(db: Session, reader_id: int, reader_data: dict) -> Optional[Reader]:
    db_reader = get_reader(db, reader_id)
    if not db_reader:
        return None
    
    for field, value in reader_data.items():
        if value is not None:
            setattr(db_reader, field, value)
    
    db.commit()
    db.refresh(db_reader)
    return db_reader

def delete_reader(db: Session, reader_id: int) -> bool:
    db_reader = get_reader(db, reader_id)
    if not db_reader:
        return False
    
    db.delete(db_reader)
    db.commit()
    return True