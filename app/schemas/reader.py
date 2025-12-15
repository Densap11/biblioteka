from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class ReaderBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    library_card: str = Field(..., min_length=1, max_length=50)
    email: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)

class ReaderCreate(ReaderBase):
    pass

class ReaderUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    status: Optional[str] = Field(None, pattern="^(active|blocked)$")

class ReaderInDB(ReaderBase):
    id: int
    status: str = "active"
    registration_date: Optional[date] = None
    
    class Config:
        from_attributes = True