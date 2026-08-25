from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI(title="Credit Risk ML Service")

# Chargement des modèles
model = joblib.load('models/xgboost_final_regularized.pkl')
scaler = joblib.load('models/scaler_final.pkl')

class PredictRequest(BaseModel):
    features: list[float]

class PredictResponse(BaseModel):
    probability: float
    risk_score: int
    risk_category: str
    shap_values: dict

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    if len(request.features) != 35:
        raise HTTPException(status_code=400, detail="35 features required")
    
    features = np.array(request.features).reshape(1, -1)
    features_scaled = scaler.transform(features)
    proba = float(model.predict_proba(features_scaled)[0, 1])
    
    risk_score = int((1 - proba) * 100)
    if proba < 0.3:
        category = "LOW"
    elif proba < 0.5:
        category = "MEDIUM"
    else:
        category = "HIGH"
    
    # SHAP simulé (à améliorer)
    shap_values = {
        "payment_history_score": 0.55,
        "loan_to_income": 0.32,
        "LIMIT_BAL": -0.18
    }
    
    return PredictResponse(
        probability=proba,
        risk_score=risk_score,
        risk_category=category,
        shap_values=shap_values
    )