from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.models.loan import Loan
from app.models.copy import Copy

def get_loan(db: Session, loan_id: int) -> Optional[Loan]:
    return db.query(Loan).filter(Loan.id == loan_id).first()

def get_loans(db: Session, skip: int = 0, limit: int = 100) -> List[Loan]:
    return db.query(Loan).offset(skip).limit(limit).all()

def get_active_loans(db: Session) -> List[Loan]:
    return db.query(Loan).filter(Loan.status == "active").all()

def get_overdue_loans(db: Session) -> List[Loan]:
    today = date.today()
    return db.query(Loan).filter(
        Loan.status == "active",
        Loan.due_date < today
    ).all()

def get_reader_loans(db: Session, reader_id: int) -> List[Loan]:
    return db.query(Loan).filter(Loan.reader_id == reader_id).all()

def get_active_reader_loans(db: Session, reader_id: int) -> List[Loan]:
    return db.query(Loan).filter(
        Loan.reader_id == reader_id,
        Loan.status == "active"
    ).all()

def create_loan(db: Session, loan_data: dict) -> Loan:
    db_loan = Loan(**loan_data)
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def update_loan(db: Session, loan_id: int, loan_data: dict) -> Optional[Loan]:
    db_loan = get_loan(db, loan_id)
    if not db_loan:
        return None
    
    for field, value in loan_data.items():
        if value is not None:
            setattr(db_loan, field, value)
    
    db.commit()
    db.refresh(db_loan)
    return db_loan

def delete_loan(db: Session, loan_id: int) -> bool:
    db_loan = get_loan(db, loan_id)
    if not db_loan:
        return False
    
    db.delete(db_loan)
    db.commit()
    return True

def can_borrow_more(db: Session, reader_id: int, max_books: int = 5) -> bool:
    """Проверяет, может ли читатель взять еще книги"""
    active_loans_count = db.query(Loan).filter(
        Loan.reader_id == reader_id,
        Loan.status == "active"
    ).count()
    return active_loans_count < max_books

def is_copy_available(db: Session, copy_id: int) -> bool:
    """Проверяет, доступен ли экземпляр для выдачи"""
    copy = db.query(Copy).filter(Copy.id == copy_id).first()
    if not copy:
        return False
    return copy.status == "available"