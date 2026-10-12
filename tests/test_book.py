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


def test_filter_by_name(client, author_id):
    client.post("/books/", json={
        "name": "Dom Casmurro",
        "edition": "1st",
        "publication_year": 1899,
        "authors": [author_id]
    })
    client.post("/books/", json={
        "name": "Memórias Póstumas de Brás Cubas",
        "edition": "1st",
        "publication_year": 1881,
        "authors": [author_id]
    })
    response = client.get("/books/?name=Dom")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Dom Casmurro"


def test_filter_by_year(client, author_id):
    client.post("/books/", json={
        "name": "Dom Casmurro",
        "edition": "1st",
        "publication_year": 1899,
        "authors": [author_id]
    })
    client.post("/books/", json={
        "name": "Memórias Póstumas de Brás Cubas",
        "edition": "1st",
        "publication_year": 1881,
        "authors": [author_id]
    })
    response = client.get("/books/?publication_year=1899")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Dom Casmurro"


def test_filter_by_author(client, author_id):
    author_response = client.post("/authors/", json={"name": "Shakespeare"})
    shakespeare_id = author_response.json()["id"]
    client.post("/books/", json={
        "name": "Dom Casmurro",
        "edition": "1st",
        "publication_year": 1899,
        "authors": [author_id]
    })
    client.post("/books/", json={
        "name": "Hamlet",
        "edition": "1st",
        "publication_year": 1603,
        "authors": [shakespeare_id]
    })

    response = client.get(f"/books/?authors_name=Shakespeare")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Hamlet"
    assert len(response.json()[0]["authors"]) == 1
    assert response.json()[0]["authors"][0]["id"] == shakespeare_id
    assert response.json()[0]["authors"][0]["name"] == "Shakespeare"


def test_list_books_without_filters(client, author_id):
    client.post("/books/", json={
        "name": "Dom Casmurro",
        "edition": "1st",
        "publication_year": 1899,
        "authors": [author_id]
    })

    client.post("/books/", json={
        "name": "Memórias Póstumas de Brás Cubas",
        "edition": "1st",
        "publication_year": 1881,
        "authors": [author_id]
    })

    response = client.get(f"/books/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_create_book_with_invalid_author(client):
    response = client.post("/books/", json={
        "name": "Dom Casmurro",
        "edition": "1st",
        "publication_year": 1899,
        "authors": [9999]
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Author not found"


def test_update_book_with_invalid_author(client, author_id):
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
        "authors": [9999]
    })
    assert update_response.status_code == 404
    assert update_response.json()["detail"] == "Author not found"


def test_list_books_pagination(client, author_id):
    for i in range(5):
        client.post("/books/", json={"name": f"Book {i}", "edition": "1st", "publication_year": 1900 + i, "authors": [author_id]})
    response = client.get("/books/?skip=2&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Book 2"
    assert response.json()[1]["name"] == "Book 3"
    
