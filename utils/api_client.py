"""
Client pour l'API Spring Boot (cf. cahier des charges §6).
Toutes les fonctions respectent le contrat décrit dans le PDF (POST /api/predict,
GET /api/history, GET /api/metrics). En USE_MOCK=True elles renvoient des données
simulées avec la même forme exacte que l'API réelle, pour un basculement transparent.
"""

import random
from datetime import datetime, timedelta

import requests
import streamlit as st

from utils.config import USE_MOCK, API_BASE_URL, ENDPOINTS, API_TIMEOUT


class ApiError(Exception):
    pass


def _auth():
    return (st.session_state.get("username", ""), st.session_state.get("_password", ""))

def build_feature_vector(form: dict) -> list:
    limit_bal = form["limit_bal"]
    sex = 1 if form["sex"] == "Homme" else 2
    education = {"Graduate School": 1, "Université": 2, "Lycée": 3, "Autre": 4}[form["education"]]
    marriage = {"Marié": 1, "Célibataire": 2, "Autre": 3}[form["marriage"]]
    age = form["age"]

    pay_status = form["pay_status"]  # liste de 6 int
    bill_amt = form["bill_amt"]  # liste de 6 float
    pay_amt = form["pay_amt"]  # liste de 6 float

    total_bill = sum(bill_amt)
    total_paid = sum(pay_amt)
    avg_bill = total_bill / 6
    avg_paid = total_paid / 6

    # Features "engineered" (12 dernières valeurs du vecteur de 35)
    late_ratio = sum(1 for p in pay_status if p > 0) / 6
    payment_history_score = 1 - late_ratio
    utilization_1 = (bill_amt[0] / limit_bal) if limit_bal else 0
    utilization_2 = (bill_amt[1] / limit_bal) if limit_bal else 0
    utilization_3 = (bill_amt[2] / limit_bal) if limit_bal else 0
    repayment_ratio = (total_paid / total_bill) if total_bill else 0
    max_delay = max(pay_status)
    loan_to_income_proxy = (avg_bill / (avg_paid + 1)) if avg_paid >= 0 else avg_bill

    return [
        limit_bal, sex, education, marriage, age,
        *pay_status,               # 6
        *bill_amt,                 # 6
        *pay_amt,                  # 6
        payment_history_score,
        utilization_1, utilization_2, utilization_3,
        repayment_ratio,
        max_delay,
        late_ratio * 100,
        total_bill,
        total_paid,
        avg_bill,
        loan_to_income_proxy if loan_to_income_proxy <= 10 else 10,
        max_delay,
    ]


# --- MOCK helpers ---------------------------------------------------------
def _mock_predict(features: list) -> dict:
    late_ratio = features[27] if len(features) > 27 else 0.2
    proba = max(0.02, min(0.95, 0.15 + late_ratio * 0.4 + random.uniform(-0.05, 0.05)))
    score = round(proba * 100)
    category = "LOW" if score < 35 else ("MEDIUM" if score < 65 else "HIGH")
    return {
        "probabilityOfDefault": round(proba, 4),
        "riskScore": score,
        "riskCategory": category,
        "shapExplanation": {
            "payment_history_score": round(random.uniform(0.2, 0.6), 2),
            "loan_to_income": round(random.uniform(-0.4, 0.4), 2),
            "LIMIT_BAL": round(random.uniform(-0.3, 0.1), 2),
            "utilization_1": round(random.uniform(-0.2, 0.3), 2),
            "AGE": round(random.uniform(-0.1, 0.1), 2),
        },
        "timestamp": datetime.now().isoformat(),
        "modelVersion": "v1.0.0-mock",
    }


def _mock_history(n: int = 20, full: bool = False) -> list:
    rows = []
    for i in range(n):
        score = random.randint(5, 95)
        category = "LOW" if score < 35 else ("MEDIUM" if score < 65 else "HIGH")
        row = {
            "date": (datetime.now() - timedelta(hours=i * 3)).strftime("%Y-%m-%d %H:%M"),
            "clientId": f"CLI-{1000 + i}",
            "probabilityOfDefault": round(score / 100, 2),
            "riskCategory": category,
            "decisionStatus": random.choice(["Acceptée", "Référée", "Refusée", "En attente"]),
        }
        if full:
            row["agent"] = random.choice(["Agent Dupont", "Agent Mbarga", "Agent Njoya"])
        rows.append(row)
    return rows


def _mock_metrics() -> dict:
    return {
        "rocAuc": 0.7634,
        "confusionMatrix": [[4140, 533], [704, 623]],
        "brierScore": 0.18,
        "total": 5987,
        "avg_default": 0.221,
        "pct_high": 0.104,
        "referred": 612,
        "shapGlobal": {
            "payment_history_score": 0.31,
            "loan_to_income": 0.24,
            "LIMIT_BAL": 0.18,
            "utilization_1": 0.14,
            "AGE": 0.09,
            "repayment_ratio": 0.08,
            "max_delay": 0.07,
            "EDUCATION": 0.05,
            "MARRIAGE": 0.04,
            "avg_bill": 0.03,
        },
        "timeline": [
            {"period": f"S{i+1}", "avg_default": round(random.uniform(0.15, 0.28), 3)}
            for i in range(12)
        ],
    }


# --- API publique ----------------------------------------------------------
def post_predict(form: dict) -> dict:
    features = build_feature_vector(form)
    if USE_MOCK:
        return _mock_predict(features)
    try:
        resp = requests.post(
            f"{API_BASE_URL}{ENDPOINTS['predict']}",
            json={"features": features},
            auth=_auth(),
            timeout=API_TIMEOUT,
        )
        if resp.status_code == 401:
            raise ApiError("Session expirée, reconnectez-vous.")
        if resp.status_code == 400:
            raise ApiError("Format de requête invalide.")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        raise ApiError("Service temporairement indisponible.")


def get_history(full: bool = False, limit: int = 20) -> list:
    if USE_MOCK:
        return _mock_history(limit, full=full)
    try:
        resp = requests.get(
            f"{API_BASE_URL}{ENDPOINTS['history']}",
            params={"limit": limit, "scope": "all" if full else "own"},
            auth=_auth(),
            timeout=API_TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        raise ApiError("Service temporairement indisponible.")


def get_metrics() -> dict:
    if USE_MOCK:
        return _mock_metrics()
    try:
        resp = requests.get(
            f"{API_BASE_URL}{ENDPOINTS['metrics']}",
            auth=_auth(),
            timeout=API_TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        raise ApiError("Service temporairement indisponible.")
