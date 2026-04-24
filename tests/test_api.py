from contextlib import asynccontextmanager
import numpy as np
from fastapi.testclient import TestClient
import pytest
import app.main as main_app


class DummyScaler:
    def transform(self, input_df):
        return input_df.values


class DummyModel:
    def predict(self, dmatrix):
        return np.array([0.8])

@pytest.fixture
def client(monkeypatch):
    @asynccontextmanager
    async def noop_lifespan(_app):
        yield

    # Avoid loading filesystem artifacts during tests.
    monkeypatch.setattr(main_app.app.router, "lifespan_context", noop_lifespan)
    monkeypatch.setattr(main_app, "scaler", DummyScaler())
    monkeypatch.setattr(main_app, "model", DummyModel())

    with TestClient(main_app.app) as test_client:
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