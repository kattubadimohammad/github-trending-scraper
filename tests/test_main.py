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

def test_root():
    # Test the root endpoint
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Welcome to the GitHub Trending Scraper API"

def test_health_check():
    # Test the health check endpoint
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
