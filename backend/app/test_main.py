from fastapi.testclient import TestClient
import os
import sys

# Ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_model_info():
    response = client.get("/api/model/info")
    # Even if not available, should return 200
    assert response.status_code == 200
