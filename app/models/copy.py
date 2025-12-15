from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Copy(Base):
    """Модель экземпляра книги"""
    
    __tablename__ = "copies"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    inventory_number = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(
        String(20), 
        nullable=False, 
        default="available",
        index=True
    )  # available, borrowed, under_repair, written_off
    acquisition_date = Column(Date, server_default=func.current_date())
    
    # Связи
    book = relationship("Book", backref="copies")
    
    def __repr__(self):
        return f"<Copy(id={self.id}, inv='{self.inventory_number}', status='{self.status}')>"