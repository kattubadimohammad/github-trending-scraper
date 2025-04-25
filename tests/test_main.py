from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_analyze_trending():
    # Test the API for a valid language, e.g., 'python'
    response = client.get("/analyze/github/trending/python")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "edges" in data
    assert len(data["nodes"]) > 0
    assert len(data["edges"]) > 0
