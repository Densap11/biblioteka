from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import func
from app.database import Base

class Librarian(Base):
    """Модель сотрудника библиотеки"""
    
    __tablename__ = "librarians"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    position = Column(String(100))
    login = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(
        String(20), 
        nullable=False, 
        default="librarian",
        index=True
    )  # librarian, admin
    created_at = Column(String, server_default=func.now())
    
    def __repr__(self):
        return f"<Librarian(id={self.id}, login='{self.login}', role='{self.role}')>"