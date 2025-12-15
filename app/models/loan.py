from sqlalchemy import Column, Integer, String, Date, ForeignKey  # Добавили String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Loan(Base):
    """Модель выдачи книги"""
    
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)
    copy_id = Column(Integer, ForeignKey("copies.id", ondelete="CASCADE"), nullable=False)
    reader_id = Column(Integer, ForeignKey("readers.id", ondelete="CASCADE"), nullable=False)
    librarian_id = Column(Integer, ForeignKey("librarians.id", ondelete="SET NULL"))
    
    # Даты
    loan_date = Column(Date, nullable=False, server_default=func.current_date())
    due_date = Column(Date, nullable=False)
    return_date = Column(Date)
    
    # Статус
    status = Column(
        String(20), 
        nullable=False, 
        default="active",
        index=True
    )  # active, returned, overdue
    
    # Связи
    copy = relationship("Copy", backref="loans")
    reader = relationship("Reader", backref="loans")
    librarian = relationship("Librarian", backref="loans")
    
    def __repr__(self):
        return f"<Loan(id={self.id}, copy_id={self.copy_id}, reader_id={self.reader_id})>"