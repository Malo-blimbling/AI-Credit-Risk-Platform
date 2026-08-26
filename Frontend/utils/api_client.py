"""Client HTTP pour l'API Spring Boot."""

import requests
import streamlit as st

from utils.config import API_BASE_URL, ENDPOINTS, API_TIMEOUT


class ApiError(Exception):
    pass


def _auth():
    return st.session_state.get("credentials")

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


# --- API publique ----------------------------------------------------------
def post_predict(form: dict) -> dict:
    features = build_feature_vector(form)
    try:
        resp = requests.post(
            f"{API_BASE_URL}{ENDPOINTS['predict']}",
            json={"features": features},
            auth=_auth(),
            timeout=API_TIMEOUT,
        )
        if resp.status_code in (401, 403):
            raise ApiError("Session expirée, reconnectez-vous.")
        if resp.status_code == 400:
            raise ApiError("Format de requête invalide.")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException:
        raise ApiError("Service temporairement indisponible.")


def get_history(full: bool = False, limit: int = 20) -> list:
    try:
        resp = requests.get(
            f"{API_BASE_URL}{ENDPOINTS['history']}",
            params={"limit": limit, "scope": "all" if full else "own"},
            auth=_auth(),
            timeout=API_TIMEOUT,
        )
        if resp.status_code in (401, 403):
            raise ApiError("Accès non autorisé pour cet historique.")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException:
        raise ApiError("Service temporairement indisponible.")


def get_metrics() -> dict:
    try:
        resp = requests.get(
            f"{API_BASE_URL}{ENDPOINTS['metrics']}",
            auth=_auth(),
            timeout=API_TIMEOUT,
        )
        if resp.status_code in (401, 403):
            raise ApiError("Accès non autorisé aux indicateurs.")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException:
        raise ApiError("Service temporairement indisponible.")
