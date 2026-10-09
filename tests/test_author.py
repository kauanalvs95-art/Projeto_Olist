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