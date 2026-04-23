# XGBoost Anomaly Detection API

An end-to-end machine learning engineering project that trains an XGBoost classifier on tabular sensor data and deploys it as a production-ready REST API using FastAPI and Docker.

##  Overview
This repository demonstrates the transition of a machine learning model from exploratory data analysis into a deployable software artifact. The model analyzes numeric features (e.g., sensor momentum, trajectory angles) to classify high-dimensional observations as either anomalous (1) or baseline (0).

**Key Engineering Practices Highlighted:**
* **Modular Pipeline:** Separation of data preparation, model training, and API serving logic.
* **Artifact Management:** Saving both the trained model weights and the data scaler (`StandardScaler`) to ensure production data is transformed identically to training data.
* **Data Validation:** Strict schema enforcement on incoming API requests using Pydantic.
* **Containerization:** Packaged via Docker for consistent deployment across environments.

## Project Status & Roadmap
- [x] **Modular Training Pipeline:** Separated logic into `src/train.py` and `src/config.py`.
- [x] **Artifact Management:** Scaler and Model serialization to `/models`.
- [x] **Data Validation:** Strict schema enforcement via Pydantic.
- [x] **REST API:** Inference serving via FastAPI.
- [ ] **Containerization:** Production packaging with Docker.

## Tech Stack
* **Machine Learning:** XGBoost, Scikit-Learn, Pandas, NumPy
* **API Framework:** FastAPI, Uvicorn, Pydantic
* **Environment Management:** uv
* **Infrastructure:** Docker, Linux
* **Version Control:** Git

## Repository Structure
```text
├── src/                      # ML training code
│   ├── train.py              # Script to train XGBoost and save artifacts
│   └── config.py             # Configuration constants (e.g., feature mappings)
├── models/                   # Saved ML artifacts (ignored in git)
│   ├── model.json            # XGBoost model weights
│   └── scaler.pkl            # Fitted StandardScaler
├── tests/
│   ├── __init__.py
│   ├── test_logic.py    # Tests for training/scaling logic
│   └── test_api.py      # Tests for FastAPI endpoints
├── data/                     # Local Data (Git-ignored)
├── pyproject.toml            # Project dependencies (managed by uv)
├── uv.lock                   # Deterministic dependency lockfile
└── README.md