from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta

from app.database import get_db
from app.models.loan import Loan
from app.models.copy import Copy
from app.models.reader import Reader
from app.models.book import Book
from app.schemas.loan import LoanCreate, LoanInDB, LoanUpdate

router = APIRouter()

@router.get("/", response_model=List[LoanInDB])
def read_loans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: str = Query(None, description="Фильтр по статусу"),
    db: Session = Depends(get_db)
):
    """Получить список всех выдач"""
    query = db.query(Loan)
    
    if status:
        query = query.filter(Loan.status == status)
    
    loans = query.offset(skip).limit(limit).all()
    
    # Добавляем дополнительную информацию
    result = []
    for loan in loans:
        loan_dict = loan.__dict__.copy()
        
        # Информация об экземпляре и книге
        copy = db.query(Copy).filter(Copy.id == loan.copy_id).first()
        if copy:
            loan_dict["copy_inventory"] = copy.inventory_number
            book = db.query(Book).filter(Book.id == copy.book_id).first()
            if book:
                loan_dict["book_title"] = book.title
        
        # Информация о читателе
        reader = db.query(Reader).filter(Reader.id == loan.reader_id).first()
        if reader:
            loan_dict["reader_name"] = reader.full_name
        
        result.append(LoanInDB(**loan_dict))
    
    return result

@router.get("/{loan_id}", response_model=LoanInDB)
def read_loan(loan_id: int, db: Session = Depends(get_db)):
    """Получить выдачу по ID"""
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if loan is None:
        raise HTTPException(status_code=404, detail="Выдача не найдена")
    
    loan_dict = loan.__dict__.copy()
    
    # Добавляем дополнительную информацию
    copy = db.query(Copy).filter(Copy.id == loan.copy_id).first()
    if copy:
        loan_dict["copy_inventory"] = copy.inventory_number
        book = db.query(Book).filter(Book.id == copy.book_id).first()
        if book:
            loan_dict["book_title"] = book.title
    
    reader = db.query(Reader).filter(Reader.id == loan.reader_id).first()
    if reader:
        loan_dict["reader_name"] = reader.full_name
    
    return LoanInDB(**loan_dict)

@router.get("/reader/{reader_id}/active", response_model=List[LoanInDB])
def read_active_reader_loans(reader_id: int, db: Session = Depends(get_db)):
    """Получить активные выдачи читателя"""
    loans = db.query(Loan).filter(
        Loan.reader_id == reader_id,
        Loan.status == "active"
    ).all()
    
    result = []
    for loan in loans:
        loan_dict = loan.__dict__.copy()
        
        copy = db.query(Copy).filter(Copy.id == loan.copy_id).first()
        if copy:
            loan_dict["copy_inventory"] = copy.inventory_number
            book = db.query(Book).filter(Book.id == copy.book_id).first()
            if book:
                loan_dict["book_title"] = book.title
        
        reader = db.query(Reader).filter(Reader.id == loan.reader_id).first()
        if reader:
            loan_dict["reader_name"] = reader.full_name
        
        result.append(LoanInDB(**loan_dict))
    
    return result

@router.get("/overdue/", response_model=List[LoanInDB])
def read_overdue_loans(db: Session = Depends(get_db)):
    """Получить просроченные выдачи"""
    today = date.today()
    loans = db.query(Loan).filter(
        Loan.status == "active",
        Loan.due_date < today
    ).all()
    
    result = []
    for loan in loans:
        loan_dict = loan.__dict__.copy()
        
        copy = db.query(Copy).filter(Copy.id == loan.copy_id).first()
        if copy:
            loan_dict["copy_inventory"] = copy.inventory_number
            book = db.query(Book).filter(Book.id == copy.book_id).first()
            if book:
                loan_dict["book_title"] = book.title
        
        reader = db.query(Reader).filter(Reader.id == loan.reader_id).first()
        if reader:
            loan_dict["reader_name"] = reader.full_name
        
        result.append(LoanInDB(**loan_dict))
    
    return result

@router.post("/", response_model=LoanInDB, status_code=201)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    """Создать новую выдачу (взять книгу)"""
    # Проверяем существование читателя
    reader = db.query(Reader).filter(Reader.id == loan.reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    
    # Проверяем статус читателя
    if reader.status == "blocked":
        raise HTTPException(status_code=400, detail="Читатель заблокирован")
    
    # Проверяем существование экземпляра
    copy = db.query(Copy).filter(Copy.id == loan.copy_id).first()
    if not copy:
        raise HTTPException(status_code=404, detail="Экземпляр не найден")
    
    # Проверяем доступность экземпляра
    if copy.status != "available":
        raise HTTPException(status_code=400, detail="Экземпляр недоступен для выдачи")
    
    # Проверяем лимит книг у читателя (максимум 5)
    active_loans_count = db.query(Loan).filter(
        Loan.reader_id == loan.reader_id,
        Loan.status == "active"
    ).count()
    
    if active_loans_count >= 5:
        raise HTTPException(status_code=400, detail="Превышен лимит книг (максимум 5)")
    
    # Создаем выдачу
    today = date.today()
    due_date = today + timedelta(days=loan.loan_days)
    
    db_loan = Loan(
        copy_id=loan.copy_id,
        reader_id=loan.reader_id,
        loan_date=today,
        due_date=due_date,
        status="active"
    )
    
    db.add(db_loan)
    
    # Меняем статус экземпляра
    copy.status = "borrowed"
    
    db.commit()
    db.refresh(db_loan)
    
    # Добавляем дополнительную информацию для ответа
    loan_dict = db_loan.__dict__.copy()
    loan_dict["copy_inventory"] = copy.inventory_number
    
    book = db.query(Book).filter(Book.id == copy.book_id).first()
    if book:
        loan_dict["book_title"] = book.title
    
    loan_dict["reader_name"] = reader.full_name
    
    return LoanInDB(**loan_dict)

@router.post("/return/{loan_id}", response_model=LoanInDB)
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    """Вернуть книгу (закрыть выдачу)"""
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if loan is None:
        raise HTTPException(status_code=404, detail="Выдача не найдена")
    
    if loan.status != "active":
        raise HTTPException(status_code=400, detail="Выдача уже закрыта")
    
    # Обновляем выдачу
    loan.return_date = date.today()
    loan.status = "returned"
    
    # Возвращаем экземпляр
    copy = db.query(Copy).filter(Copy.id == loan.copy_id).first()
    if copy:
        copy.status = "available"
    
    db.commit()
    db.refresh(loan)
    
    # Добавляем дополнительную информацию для ответа
    loan_dict = loan.__dict__.copy()
    
    if copy:
        loan_dict["copy_inventory"] = copy.inventory_number
        book = db.query(Book).filter(Book.id == copy.book_id).first()
        if book:
            loan_dict["book_title"] = book.title
    
    reader = db.query(Reader).filter(Reader.id == loan.reader_id).first()
    if reader:
        loan_dict["reader_name"] = reader.full_name
    
    return LoanInDB(**loan_dict)

@router.delete("/{loan_id}", status_code=204)
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    """Удалить выдачу (только для админа)"""
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if loan is None:
        raise HTTPException(status_code=404, detail="Выдача не найден")
    
    db.delete(loan)
    db.commit()
    return None

@router.get("/stats/summary")
def get_loans_summary(db: Session = Depends(get_db)):
    """Статистика по выдачам"""
    total_loans = db.query(Loan).count()
    active_loans = db.query(Loan).filter(Loan.status == "active").count()
    overdue_loans = db.query(Loan).filter(
        Loan.status == "active",
        Loan.due_date < date.today()
    ).count()
    
    return {
        "total_loans": total_loans,
        "active_loans": active_loans,
        "overdue_loans": overdue_loans,
        "returned_loans": total_loans - active_loans
    }