import os
import sys
import traceback
import pandas as pd
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, accuracy_score

from config import PHYSICS_TO_TECH_MAP

def load_and_anonymize_data(data_path: str) -> pd.DataFrame:
    """Loads the dataset and renames physics features to generic engineering features."""
    df = pd.read_parquet(data_path)
    
    # Only keep the columns we are renaming/using to keep the payload lightweight
    df = df[list(PHYSICS_TO_TECH_MAP.keys())]
    df = df.rename(columns=PHYSICS_TO_TECH_MAP)
    
    return df

def prepare_data(df: pd.DataFrame):
    """Splits the data, fits the scaler, and SAVES the scaler artifact."""
    X = df.drop(columns=['is_anomaly'])
    y = df['is_anomaly']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # CRITICAL: Fit scaler only on training data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Save the scaler for the FastAPI app
    os.makedirs('models', exist_ok=True)
    joblib.dump(scaler, 'models/scaler.pkl')
    print("Saved fitted scaler to models/scaler.pkl")

    return X_train_scaled, X_test_scaled, y_train, y_test

def train_and_evaluate(X_train, X_test, y_train, y_test):
    """Trains XGBoost with DMatrix inputs, prints metrics, and SAVES the model."""
    print("Starting XGBoost training...")
    
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    params = {
        'max_depth': 5,
        'eta': 0.1,
        'objective': 'binary:logistic',
        'eval_metric': 'auc',
        'seed': 42
    }

    num_boost_round = 100
    model = xgb.train(
        params=params,
        dtrain=dtrain,
        num_boost_round=num_boost_round,
        evals=[(dtest, 'test')],
        verbose_eval=False
    )

    # Evaluate
    probabilities = model.predict(dtest)
    predictions = (probabilities >= 0.5).astype(int)
    
    acc = accuracy_score(y_test, predictions)
    auc = roc_auc_score(y_test, probabilities)
    
    print(f"Model Performance - Accuracy: {acc:.4f} | AUC: {auc:.4f}")

    # Save the model in JSON format (XGBoost standard)
    model.save_model('models/model.json')
    print("Saved XGBoost model to models/model.json")

if __name__ == "__main__":
    # Point to the local dataset (ensure it's in .gitignore!)
    DATA_PATH = "./data/processed_data.parquet" 
    
    try:
        print("Pipeline started...")
        df = load_and_anonymize_data(DATA_PATH)
        X_train, X_test, y_train, y_test = prepare_data(df)
        train_and_evaluate(X_train, X_test, y_train, y_test)
        print("Pipeline execution complete. Ready for API integration.")
    except Exception as e:
        print(f"Error in pipeline: {e}", file=sys.stderr)
        print(f"Exception type: {type(e).__name__}", file=sys.stderr)
        print("Traceback:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)