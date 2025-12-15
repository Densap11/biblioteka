import pytest
from fastapi import status

def test_health_check(client):
    """Тест эндпоинта проверки здоровья"""
    response = client.get("/api/health")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["status"] == "healthy"
    assert "app" in data
    assert "version" in data

def test_create_and_get_book(client, test_book_data):
    """Тест создания и получения книги"""
    # Создаем книгу
    response = client.post("/api/books/", json=test_book_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    created_book = response.json()
    
    assert created_book["title"] == test_book_data["title"]
    assert created_book["author"] == test_book_data["author"]
    assert created_book["id"] is not None
    
    # Получаем созданную книгу
    book_id = created_book["id"]
    response = client.get(f"/api/books/{book_id}")
    
    assert response.status_code == status.HTTP_200_OK
    retrieved_book = response.json()
    
    assert retrieved_book["id"] == book_id
    assert retrieved_book["title"] == test_book_data["title"]

def test_update_book(client, test_book_data):
    """Тест обновления книги"""
    # Создаем книгу
    response = client.post("/api/books/", json=test_book_data)
    book_id = response.json()["id"]
    
    # Обновляем книгу
    update_data = {"title": "Обновленное название", "year": 2025}
    response = client.put(f"/api/books/{book_id}", json=update_data)
    
    assert response.status_code == status.HTTP_200_OK
    updated_book = response.json()
    
    assert updated_book["title"] == "Обновленное название"
    assert updated_book["year"] == 2025
    assert updated_book["author"] == test_book_data["author"]  # Осталось прежним

def test_delete_book(client, test_book_data):
    """Тест удаления книги"""
    # Создаем книгу
    response = client.post("/api/books/", json=test_book_data)
    book_id = response.json()["id"]
    
    # Удаляем книгу
    response = client.delete(f"/api/books/{book_id}")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Проверяем, что книга удалена
    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_search_books(client, test_book_data):
    """Тест поиска книг"""
    # Создаем книгу для поиска
    response = client.post("/api/books/", json=test_book_data)
    
    # Ищем по названию
    response = client.get("/api/books/search/?q=Тестовая")
    
    assert response.status_code == status.HTTP_200_OK
    books = response.json()
    
    assert len(books) > 0
    assert any(book["title"] == test_book_data["title"] for book in books)

def test_create_and_get_reader(client, test_reader_data):
    """Тест создания и получения читателя"""
    # Создаем читателя
    response = client.post("/api/readers/", json=test_reader_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    created_reader = response.json()
    
    assert created_reader["full_name"] == test_reader_data["full_name"]
    assert created_reader["library_card"] == test_reader_data["library_card"]
    assert created_reader["status"] == "active"
    
    # Получаем по номеру билета
    response = client.get(f"/api/readers/card/{test_reader_data['library_card']}")
    
    assert response.status_code == status.HTTP_200_OK
    retrieved_reader = response.json()
    
    assert retrieved_reader["library_card"] == test_reader_data["library_card"]

def test_book_loan_cycle(client):
    """Тест полного цикла выдачи книги"""
    # 1. Создаем книгу
    book_data = {
        "title": "Книга для выдачи",
        "author": "Автор",
        "year": 2024,
        "genre": "Тест"
    }
    book_response = client.post("/api/books/", json=book_data)
    book_id = book_response.json()["id"]
    
    # 2. Создаем экземпляр
    copy_data = {
        "book_id": book_id,
        "inventory_number": "LOAN-TEST-001",
        "status": "available"
    }
    copy_response = client.post("/api/copies/", json=copy_data)
    copy_id = copy_response.json()["id"]
    
    # 3. Создаем читателя
    reader_data = {
        "full_name": "Читатель для выдачи",
        "library_card": "LOAN-READER-001"
    }
    reader_response = client.post("/api/readers/", json=reader_data)
    reader_id = reader_response.json()["id"]
    
    # 4. Выдаем книгу
    loan_data = {
        "copy_id": copy_id,
        "reader_id": reader_id,
        "loan_days": 14
    }
    loan_response = client.post("/api/loans/", json=loan_data)
    
    assert loan_response.status_code == status.HTTP_201_CREATED
    loan = loan_response.json()
    
    assert loan["status"] == "active"
    assert loan["return_date"] is None
    
    # 5. Проверяем, что экземпляр стал недоступен
    copy_response = client.get(f"/api/copies/{copy_id}")
    assert copy_response.json()["status"] == "borrowed"
    
    # 6. Возвращаем книгу
    return_response = client.post(f"/api/loans/return/{loan['id']}")
    
    assert return_response.status_code == status.HTTP_200_OK
    returned_loan = return_response.json()
    
    assert returned_loan["status"] == "returned"
    assert returned_loan["return_date"] is not None
    
    # 7. Проверяем, что экземпляр снова доступен
    copy_response = client.get(f"/api/copies/{copy_id}")
    assert copy_response.json()["status"] == "available"

def test_reader_book_limit(client):
    """Тест лимита книг у читателя"""
    # Создаем читателя
    reader_data = {
        "full_name": "Читатель с лимитом",
        "library_card": "LIMIT-001"
    }
    reader_response = client.post("/api/readers/", json=reader_data)
    reader_id = reader_response.json()["id"]
    
    # Создаем 5 экземпляров и выдаем их
    for i in range(5):
        # Книга
        book_data = {
            "title": f"Книга {i}",
            "author": "Автор",
            "year": 2024
        }
        book_response = client.post("/api/books/", json=book_data)
        book_id = book_response.json()["id"]
        
        # Экземпляр
        copy_data = {
            "book_id": book_id,
            "inventory_number": f"LIMIT-{i:03d}",
            "status": "available"
        }
        copy_response = client.post("/api/copies/", json=copy_data)
        copy_id = copy_response.json()["id"]
        
        # Выдача
        loan_data = {
            "copy_id": copy_id,
            "reader_id": reader_id,
            "loan_days": 14
        }
        loan_response = client.post("/api/loans/", json=loan_data)
        assert loan_response.status_code == status.HTTP_201_CREATED
    
    # Шестая выдача должна быть отклонена
    # Создаем еще одну книгу и экземпляр
    book_data = {
        "title": "Шестая книга",
        "author": "Автор",
        "year": 2024
    }
    book_response = client.post("/api/books/", json=book_data)
    book_id = book_response.json()["id"]
    
    copy_data = {
        "book_id": book_id,
        "inventory_number": "LIMIT-006",
        "status": "available"
    }
    copy_response = client.post("/api/copies/", json=copy_data)
    copy_id = copy_response.json()["id"]
    
    # Попытка выдать шестую книгу
    loan_data = {
        "copy_id": copy_id,
        "reader_id": reader_id,
        "loan_days": 14
    }
    loan_response = client.post("/api/loans/", json=loan_data)
    
    # Должна быть ошибка о превышении лимита
    assert loan_response.status_code == status.HTTP_400_BAD_REQUEST
    assert "лимит" in loan_response.json()["detail"].lower()