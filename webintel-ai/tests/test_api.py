from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_invalid_url():
    response = client.post("/link-analysis", json={"url":"not-a-url"})
    assert response.status_code == 422
