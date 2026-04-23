# app/main.py
import os
from contextlib import asynccontextmanager
import joblib
import xgboost as xgb
import pandas as pd
from fastapi import FastAPI, HTTPException
from .schemas import SensorData, PredictionResponse

# 1. Global variables for the model and scaler
# We load them once when the app starts, not every time a request comes in
MODEL_PATH = "models/model.json"
SCALER_PATH = "models/scaler.pkl"

model = None
scaler = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, scaler
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        raise RuntimeError("Model or Scaler artifacts not found. Run training first.")
    
    # Load XGBoost Booster
    model = xgb.Booster()
    model.load_model(MODEL_PATH)
    
    # Load Scikit-Learn Scaler
    scaler = joblib.load(SCALER_PATH)
    print("Model and Scaler loaded successfully.")
    yield

# 2. Initialize FastAPI app
app = FastAPI(
    title="Sensor Anomaly Detection API",
    description="API for classifying sensor events as signal or background using XGBoost.",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/")
def read_root():
    return {"message": "Sensor Anomaly Detection API is live. Visit /docs for documentation."}

@app.post("/predict", response_model=PredictionResponse)
def predict(data: SensorData):
    # 1. Convert Pydantic model to Dictionary, then to DataFrame
    input_dict = data.model_dump()
    input_df = pd.DataFrame([input_dict])
    
    # 2. Scale the input data using the loaded scaler
    try:
        scaled_data = scaler.transform(input_df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Scaling error: {e}")
    
    # 3. Convert to DMatrix for XGBoost Native API
    dmatrix = xgb.DMatrix(scaled_data)
    
    # 4. Run inference
    probability = float(model.predict(dmatrix)[0])
    prediction = 1 if probability > 0.5 else 0
    status = "Anomaly Detected" if prediction == 1 else "Normal Baseline"
    
    return {
        "prediction": prediction,
        "probability": round(probability, 4),
        "status": status
    }