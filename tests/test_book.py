def test_create_book(client, author_id):
    response = client.post("/books/", json={
        "name": "Dom Casmurro",
        "edition": "1st",
        "publication_year": 1899,
        "authors": [author_id]
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Dom Casmurro"
    assert response.json()["edition"] == "1st"
    assert response.json()["publication_year"] == 1899
    assert len(response.json()["authors"]) == 1
    assert response.json()["authors"][0]["id"] == author_id


def test_read_book(client, author_id):
    response = client.post("/books/", json={
        "name": "Dom Casmurro",
        "edition": "1st",
        "publication_year": 1899,
        "authors": [author_id]
    })
    book_id = response.json()["id"]
    book_response = client.get(f"/books/{book_id}")
    assert book_response.status_code == 200
    assert book_response.json()["name"] == "Dom Casmurro"
    assert book_response.json()["edition"] == "1st"
    assert book_response.json()["publication_year"] == 1899
    assert len(book_response.json()["authors"]) == 1
    assert book_response.json()["authors"][0]["id"] == author_id


def test_read_book_not_found(client):
    book_response = client.get("/books/999")
    assert book_response.status_code == 404
    assert book_response.json()["detail"] == "Book not found"


def test_update_book(client, author_id):
    response = client.post("/books/", json={
        "name": "Dom Casmurro",
        "edition": "1st",
        "publication_year": 1899,
        "authors": [author_id]
    })
    book_id = response.json()["id"]
    update_response = client.put(f"/books/{book_id}", json={
        "name": "Updated Book",
        "edition": "2nd",
        "publication_year": 1900,
        "authors": [author_id]
    })
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Book"
    assert update_response.json()["edition"] == "2nd"
    assert update_response.json()["publication_year"] == 1900
    assert len(update_response.json()["authors"]) == 1
    assert update_response.json()["authors"][0]["id"] == author_id


def test_delete_book(client, author_id):
    response = client.post("/books/", json={
        "name": "Dom Casmurro",
        "edition": "1st",
        "publication_year": 1899,
        "authors": [author_id]
    })
    book_id = response.json()["id"]
    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 200
    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404
    assert delete_response.json()["detail"] == "Book deleted successfully"