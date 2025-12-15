from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class LoanBase(BaseModel):
    copy_id: int = Field(..., ge=1, description="ID экземпляра")
    reader_id: int = Field(..., ge=1, description="ID читателя")

class LoanCreate(LoanBase):
    loan_days: int = Field(14, ge=1, le=90, description="Срок выдачи в днях")

class LoanUpdate(BaseModel):
    return_date: Optional[date] = None

class LoanInDB(LoanBase):
    id: int
    loan_date: date
    due_date: date
    return_date: Optional[date] = None
    status: str = "active"
    book_title: Optional[str] = None
    reader_name: Optional[str] = None
    copy_inventory: Optional[str] = None
    
    class Config:
        from_attributes = True