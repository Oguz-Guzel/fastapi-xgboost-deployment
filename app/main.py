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
ARTIFACT_DIR = os.getenv("MODEL_ARTIFACT_DIR", "models")
MODEL_FILE = "model.json"
SCALER_FILE = "scaler.pkl"
MODEL_PATH = os.path.join(ARTIFACT_DIR, MODEL_FILE)
SCALER_PATH = os.path.join(ARTIFACT_DIR, SCALER_FILE)

HF_MODEL_REPO_ID = os.getenv("HF_MODEL_REPO_ID", "").strip()
HF_MODEL_REVISION = os.getenv("HF_MODEL_REVISION", "main").strip() or "main"

model = None
scaler = None


def ensure_artifacts_available() -> tuple[str, str]:
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        return MODEL_PATH, SCALER_PATH

    if not HF_MODEL_REPO_ID:
        return MODEL_PATH, SCALER_PATH

    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        print("huggingface_hub is not installed; cannot download model artifacts.")
        return MODEL_PATH, SCALER_PATH

    os.makedirs(ARTIFACT_DIR, exist_ok=True)

    try:
        model_path = hf_hub_download(
            repo_id=HF_MODEL_REPO_ID,
            filename=MODEL_FILE,
            revision=HF_MODEL_REVISION,
            local_dir=ARTIFACT_DIR,
        )
        scaler_path = hf_hub_download(
            repo_id=HF_MODEL_REPO_ID,
            filename=SCALER_FILE,
            revision=HF_MODEL_REVISION,
            local_dir=ARTIFACT_DIR,
        )
        print(
            f"Downloaded model artifacts from {HF_MODEL_REPO_ID}@{HF_MODEL_REVISION} "
            f"to {ARTIFACT_DIR}."
        )
        return model_path, scaler_path
    except Exception as exc:
        print(f"Failed to download model artifacts: {exc}")
        return MODEL_PATH, SCALER_PATH

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, scaler
    artifact_model_path, artifact_scaler_path = ensure_artifacts_available()

    if not os.path.exists(artifact_model_path) or not os.path.exists(artifact_scaler_path):
        # Keep the API process alive in environments where artifacts are mounted later.
        model = None
        scaler = None
        print("Model or Scaler artifacts not found. /predict will return 503 until artifacts are available.")
        yield
        return
    
    try:
        # Load XGBoost Booster
        model = xgb.Booster()
        model.load_model(artifact_model_path)

        # Load Scikit-Learn Scaler
        scaler = joblib.load(artifact_scaler_path)
        print("Model and Scaler loaded successfully.")
    except Exception as exc:
        model = None
        scaler = None
        print(f"Failed to load model artifacts: {exc}")

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
    if model is None or scaler is None:
        raise HTTPException(
            status_code=503,
            detail="Model service unavailable: artifacts are not loaded yet."
        )

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