from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_book():
    response = client.post("/books", json={"title": "Test Book", "author": "Author", "genre": "Fiction", "year_published": 2021})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"

# Add more tests for other endpoints
