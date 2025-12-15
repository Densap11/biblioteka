from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class CopyBase(BaseModel):
    book_id: int = Field(..., ge=1, description="ID книги")
    inventory_number: str = Field(..., min_length=1, max_length=50, description="Инвентарный номер")
    status: str = Field("available", description="Статус: available, borrowed, under_repair, written_off")

class CopyCreate(CopyBase):
    pass

class CopyUpdate(BaseModel):
    status: Optional[str] = Field(None, description="Статус: available, borrowed, under_repair, written_off")

class CopyInDB(CopyBase):
    id: int
    acquisition_date: Optional[date] = None
    book_title: Optional[str] = None  # Добавим название книги для удобства
    
    class Config:
        from_attributes = True