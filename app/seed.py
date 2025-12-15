from app.database import SessionLocal
from app.models.book import Book
from app.models.copy import Copy
from app.models.reader import Reader
from app.models.loan import Loan
from datetime import date, timedelta

def seed_database():
    db = SessionLocal()
    
    try:
        print("🌱 Начинаем заполнение базы данных...")
        
        # 1. Книги
        if db.query(Book).count() == 0:
            books_data = [
                {
                    "title": "Мастер и Маргарита",
                    "author": "Михаил Булгаков",
                    "year": 1967,
                    "publisher": "Художественная литература",
                    "genre": "Роман",
                    "isbn": "978-5-699-12345-6"
                },
                {
                    "title": "Преступление и наказание", 
                    "author": "Федор Достоевский",
                    "year": 1866,
                    "publisher": "Эксмо",
                    "genre": "Роман",
                    "isbn": "978-5-04-123456-7"
                },
                {
                    "title": "Война и мир",
                    "author": "Лев Толстой",
                    "year": 1869,
                    "publisher": "АСТ",
                    "genre": "Роман-эпопея",
                    "isbn": "978-5-17-123456-8"
                }
            ]
            
            for book_data in books_data:
                book = Book(**book_data)
                db.add(book)
            
            db.commit()
            print("✅ Книги добавлены")
        
        # 2. Экземпляры
        if db.query(Copy).count() == 0:
            copies_data = [
                {"book_id": 1, "inventory_number": "INV-001", "status": "available"},
                {"book_id": 1, "inventory_number": "INV-002", "status": "available"},
                {"book_id": 2, "inventory_number": "INV-003", "status": "available"},
                {"book_id": 2, "inventory_number": "INV-004", "status": "available"},
                {"book_id": 3, "inventory_number": "INV-005", "status": "available"},
                {"book_id": 3, "inventory_number": "INV-006", "status": "under_repair"},
            ]
            
            for copy_data in copies_data:
                copy = Copy(**copy_data)
                db.add(copy)
            
            db.commit()
            print("✅ Экземпляры добавлены")
        
        # 3. Читатели
        if db.query(Reader).count() == 0:
            readers_data = [
                {
                    "full_name": "Иванов Иван Иванович",
                    "library_card": "RC-001",
                    "email": "ivanov@example.com",
                    "phone": "+79991234567"
                },
                {
                    "full_name": "Петрова Мария Сергеевна", 
                    "library_card": "RC-002",
                    "email": "petrova@example.com",
                    "phone": "+79997654321"
                },
                {
                    "full_name": "Сидоров Алексей Петрович",
                    "library_card": "RC-003",
                    "email": "sidorov@example.com",
                    "phone": "+79995554433"
                }
            ]
            
            for reader_data in readers_data:
                reader = Reader(**reader_data)
                db.add(reader)
            
            db.commit()
            print("✅ Читатели добавлены")
        
        # 4. Выдачи (опционально)
        if db.query(Loan).count() == 0:
            # Создаем тестовую выдачу
            today = date.today()
            due_date = today + timedelta(days=14)
            
            loan = Loan(
                copy_id=1,  # INV-001
                reader_id=1,  # Иванов И.И.
                loan_date=today,
                due_date=due_date,
                status="active"
            )
            db.add(loan)
            
            # Меняем статус экземпляра
            copy = db.query(Copy).filter(Copy.id == 1).first()
            if copy:
                copy.status = "borrowed"
            
            db.commit()
            print("✅ Тестовая выдача добавлена")
        
        print("🎉 База данных успешно заполнена!")
        print("📊 Статистика:")
        print(f"   📚 Книг: {db.query(Book).count()}")
        print(f"   📖 Экземпляров: {db.query(Copy).count()}")
        print(f"   👥 Читателей: {db.query(Reader).count()}")
        print(f"   📝 Выдач: {db.query(Loan).count()}")
        
    except Exception as e:
        print(f"❌ Ошибка при заполнении базы: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()