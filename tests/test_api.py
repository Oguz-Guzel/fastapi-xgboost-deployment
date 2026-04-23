from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Sensor Anomaly Detection API is live. Visit /docs for documentation."}

def test_predict_invalid_data():
    """Test if the API correctly rejects bad data (Pydantic validation)."""
    # Sending a string where a float is expected
    bad_data = {"met_E": "not-a-number"}
    response = client.post("/predict", json=bad_data)
    
    assert response.status_code == 422  # Unprocessable Entity