"""
Interface Agent de crédit (cf. cahier des charges §4).
Formulaire de saisie (35 features regroupées), résultat de prédiction avec
explication SHAP, historique personnel.
"""

import pandas as pd
import streamlit as st

from utils.auth import is_authenticated, login_page, logout, current_display_name
from utils.components import load_css, theme_picker, card_start, card_end, risk_badge, risk_gauge, app_header, error_banner
from utils.config import EDUCATION_OPTIONS, MARRIAGE_OPTIONS, SEX_OPTIONS, PAY_STATUS_OPTIONS, DECISION_MAP
from utils.api_client import post_predict, get_history, ApiError
from utils.plotting import apply_theme, shap_bar_chart

st.set_page_config(page_title="AI Credit Risk — Agent", page_icon="💳", layout="wide")
load_css(theme_picker())

# --- Authentification (§6.3 : rôle AGENT requis) ---
if not is_authenticated():
    login_page(expected_role="AGENT")
    st.stop()

if st.session_state.get("role") != "AGENT":
    error_banner("Ce compte n'a pas accès à l'interface Agent.")
    st.stop()

# --- En-tête ---
header_col, logout_col = st.columns([9, 1])
with header_col:
    app_header(current_display_name(), "Interface Agent de crédit")
with logout_col:
    if st.button("Déconnexion", use_container_width=True):
        logout()

st.markdown("<br>", unsafe_allow_html=True)

# --- Formulaire (§4.3) ---
with st.form("client_form"):
    card_start("Groupe 1 — Identité et démographie")
    c1, c2 = st.columns(2)
    with c1:
        age = st.number_input("Âge", min_value=21, max_value=79, value=35)
        sex = st.selectbox("Sexe", SEX_OPTIONS)
    with c2:
        education = st.selectbox("Niveau d'éducation", EDUCATION_OPTIONS)
        marriage = st.selectbox("Situation familiale", MARRIAGE_OPTIONS)
    card_end()

    card_start("Groupe 2 — Caractéristiques financières")
    limit_bal = st.number_input("Limite de crédit (FCFA)", min_value=0, value=500_000, step=10_000)

    st.markdown("**Montant des factures des 6 derniers mois (FCFA)**")
    bcols = st.columns(6)
    bill_amt = [bcols[i].number_input(f"Mois {i+1}", key=f"bill_{i}", value=0, step=1000) for i in range(6)]

    st.markdown("**Montant des remboursements des 6 derniers mois (FCFA)**")
    pcols = st.columns(6)
    pay_amt = [pcols[i].number_input(f"Mois {i+1}", key=f"pay_{i}", value=0, step=1000) for i in range(6)]
    card_end()

    card_start("Groupe 3 — Historique de paiement")
    st.markdown("**Statut de paiement des 6 derniers mois** (-2 = payé en avance, 0 = à jour, >0 = mois de retard)")
    scols = st.columns(6)
    pay_status = [scols[i].selectbox(f"Mois {i+1}", PAY_STATUS_OPTIONS, index=2, key=f"status_{i}") for i in range(6)]
    card_end()

    submitted = st.form_submit_button("Lancer la prédiction", use_container_width=True)

if submitted:
    form_data = {
        "age": age, "sex": sex, "education": education, "marriage": marriage,
        "limit_bal": limit_bal, "bill_amt": bill_amt, "pay_amt": pay_amt, "pay_status": pay_status,
    }
    try:
        st.session_state["last_result"] = post_predict(form_data)
    except ApiError as e:
        st.session_state.pop("last_result", None)
        error_banner(str(e))

# --- Zone de résultat (§4.4) ---
if "last_result" in st.session_state:
    result = st.session_state["last_result"]

    card_start("Résultat de la prédiction")
    col1, col2 = st.columns([1, 2])
    with col1:
        risk_gauge(result["riskScore"], result["riskCategory"])
        st.markdown(
            f'<div style="text-align:center;">{risk_badge(result["riskCategory"])}</div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<p class="mono-number" style="font-size:1.4rem; margin-bottom:.2rem;">'
            f'{result["probabilityOfDefault"]*100:.1f}%</p>'
            f'<p style="color:var(--text-secondary); margin-top:0;">probabilité de défaut</p>',
            unsafe_allow_html=True,
        )
        decision = DECISION_MAP.get(result["riskCategory"], "—")
        st.markdown(f"**Décision suggérée :** {decision}")
        st.caption(f"Modèle {result.get('modelVersion', '—')} · {result.get('timestamp', '')}")
    card_end()

    card_start("Explication SHAP")
    fig = apply_theme(shap_bar_chart(result["shapExplanation"]))
    st.plotly_chart(fig, use_container_width=True)
    card_end()

# --- Historique de l'agent (§4.5) ---
card_start("Historique de mes prédictions")
try:
    history = get_history(full=False, limit=20)
    df = pd.DataFrame(history)
    st.dataframe(df, use_container_width=True, hide_index=True)
except ApiError as e:
    error_banner(str(e))
card_end()
