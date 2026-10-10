def test_create_author(client):
    response = client.post("/authors/", json={"name": "Machado de Assis"})
    assert response.status_code == 200
    assert response.json()["name"] == "Machado de Assis"
    assert "id" in response.json()


def test_read_author(client):
    response = client.post("/authors/", json={"name": "Machado de Assis"})
    author_id = response.json()["id"]
    author_response = client.get(f"/authors/{author_id}")
    assert author_response.status_code == 200
    assert author_response.json()["name"] == "Machado de Assis"



def test_read_author_not_found(client):
    author_response = client.get("/authors/999")
    assert author_response.status_code == 404
    assert author_response.json()["detail"] == "Author not found"


def test_update_author(client):
    response = client.post("/authors/", json={"name": "Machado de Assis"})
    author_id = response.json()["id"]
    update_response = client.put(f"/authors/{author_id}", json={"name": "Updated Name"})
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Name"


def test_delete_author(client):
    response = client.post("/authors/", json={"name": "Machado de Assis"})
    author_id = response.json()["id"]
    delete_response = client.delete(f"/authors/{author_id}")
    assert delete_response.status_code == 200
    get_response = client.get(f"/authors/{author_id}")
    assert get_response.status_code == 404
    assert delete_response.json()["detail"] == "Author deleted successfully"


def test_delete_author_not_found(client):
    delete_response = client.delete("/authors/999")
    assert delete_response.status_code == 404
    assert delete_response.json()["detail"] == "Author not found"
    



def test_list_authors_pagination(client):
    for i in range(15):
        client.post("/authors/", json={"name": f"Author {i}"})
    response = client.get("/authors/?skip=5&limit=5")
    assert response.status_code == 200
    assert len(response.json()) == 5
    assert response.json()[0]["name"] == "Author 5"


def test_list_authors_search(client):
    client.post("/authors/", json={"name": "Machado de Assis"})
    client.post("/authors/", json={"name": "José de Alencar"})
    response = client.get("/authors/?author_name=Machado")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Machado de Assis"
