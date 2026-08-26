"""Configuration centrale de l'application frontend."""

import os

# --- Mode de fonctionnement ---
USE_MOCK = False

# --- API ---
API_BASE_URL = os.getenv("CREDIT_RISK_API_URL", "http://localhost:8080").rstrip("/")
API_TIMEOUT = 8  # secondes

ENDPOINTS = {
    "health": "/api/health",
    "model_info": "/api/model-info",
    "predict": "/api/predict",
    "history": "/api/history",
    "metrics": "/api/metrics",
}

# --- Identité visuelle (cf. cahier des charges §7.1) ---
COLORS = {
    "primary": "#00529B",
    "primary_dark": "#003864",
    "primary_light": "#2E7BC4",
    "low": "#1E9E5A",
    "medium": "#E8912B",
    "high": "#D93C3C",
}

FONT_FAMILY = "Inter, sans-serif"

RISK_LABELS = {"LOW": "Risque faible", "MEDIUM": "Risque modéré", "HIGH": "Risque élevé"}
RISK_ICONS = {"LOW": "🟢", "MEDIUM": "🟠", "HIGH": "🔴"}
DECISION_MAP = {"LOW": "Accepter", "MEDIUM": "Référer à un analyste", "HIGH": "Refuser"}

# --- Champs du formulaire agent (cf. cahier des charges §4.3) ---
EDUCATION_OPTIONS = ["Graduate School", "Université", "Lycée", "Autre"]
MARRIAGE_OPTIONS = ["Marié", "Célibataire", "Autre"]
SEX_OPTIONS = ["Homme", "Femme"]
PAY_STATUS_OPTIONS = list(range(-2, 9))  # -2, -1, 0, 1, ..., 8

