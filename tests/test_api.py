from fastapi.testclient import TestClient
import pytest
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

def test_read_main(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Sensor Anomaly Detection API is live. Visit /docs for documentation."}

def test_predict_invalid_type(client):
    from src.config import PHYSICS_TO_TECH_MAP
    valid_payload = {val: 0.5 for key, val in PHYSICS_TO_TECH_MAP.items() if key != 'HH'}
    
    # Intentionally change a float to a string
    valid_payload["missing_energy_magnitude"] = "REALLY_HIGH_ENERGY"
    
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 422

def test_predict_success(client):
    """Test a valid prediction request (The Happy Path)."""
    # Create a dummy payload with all 57 features
    # This ensures we aren't missing any required fields from schemas.py
    from src.config import PHYSICS_TO_TECH_MAP
    
    valid_features = {val: 0.5 for key, val in PHYSICS_TO_TECH_MAP.items() if key != 'HH'}
    
    response = client.post("/predict", json=valid_features)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probability" in data
    assert data["prediction"] in [0, 1]
    assert 0 <= data["probability"] <= 1