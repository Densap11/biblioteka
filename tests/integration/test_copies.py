from fastapi import status


def test_copies_crud(client):
    """Тест CRUD для экземпляров: создание, получение, обновление статуса и удаление"""
    # 1. Создаем книгу
    book_data = {
        "title": "Книга для экземпляров",
        "author": "Автор",
        "year": 2024
    }
    book_resp = client.post("/api/books/", json=book_data)
    assert book_resp.status_code == status.HTTP_201_CREATED
    book_id = book_resp.json()["id"]

    # 2. Создаем экземпляр
    copy_data = {
        "book_id": book_id,
        "inventory_number": "COPY-TEST-001",
        "status": "available"
    }
    resp = client.post("/api/copies/", json=copy_data)
    assert resp.status_code == status.HTTP_201_CREATED
    created = resp.json()
    copy_id = created["id"]
    assert created["inventory_number"] == copy_data["inventory_number"]

    # 3. Получаем экземпляр по ID
    resp = client.get(f"/api/copies/{copy_id}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["id"] == copy_id

    # 4. Получаем по инвентарному номеру
    resp = client.get(f"/api/copies/inventory/{copy_data['inventory_number']}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["inventory_number"] == copy_data["inventory_number"]

    # 5. Список всех экземпляров
    resp = client.get("/api/copies/?limit=100")
    assert resp.status_code == status.HTTP_200_OK
    items = resp.json()
    assert any(x["id"] == copy_id for x in items)

    # 6. Доступные экземпляры для книги
    resp = client.get(f"/api/copies/book/{book_id}/available")
    assert resp.status_code == status.HTTP_200_OK

    # 7. Пометить как выданный
    resp = client.patch(f"/api/copies/{copy_id}/mark-borrowed")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["status"] == "borrowed"

    # 8. Пометить как доступный
    resp = client.patch(f"/api/copies/{copy_id}/mark-available")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["status"] == "available"

    # 9. Удалить экземпляр
    resp = client.delete(f"/api/copies/{copy_id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    # 10. Проверяем, что 404
    resp = client.get(f"/api/copies/{copy_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
