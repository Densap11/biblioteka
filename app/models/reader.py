from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql import func
from app.database import Base

class Reader(Base):
    """Модель читателя"""
    
    __tablename__ = "readers"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False, index=True)
    library_card = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(String(255))
    status = Column(
        String(20), 
        nullable=False, 
        default="active",
        index=True
    )  # active, blocked
    registration_date = Column(Date, server_default=func.current_date())
    
    def __repr__(self):
        return f"<Reader(id={self.id}, name='{self.full_name}', card='{self.library_card}')>"