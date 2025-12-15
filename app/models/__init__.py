# Импортируем все модели для удобного доступа
from app.models.book import Book
from app.models.copy import Copy
from app.models.reader import Reader
from app.models.librarian import Librarian
from app.models.loan import Loan

# Список всех моделей для миграций
__all__ = ["Book", "Copy", "Reader", "Librarian", "Loan"]