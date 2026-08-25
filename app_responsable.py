def kpi_card(label: str, value: str):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

cols = st.columns(5)
kpis = [
    ("Demandes totales", str(metrics["total"])),
    ("Taux de défaut moyen", f"{metrics['avg_default']*100:.1f}%"),
    ("Proportion HIGH", f"{metrics['pct_high']*100:.1f}%"),
    ("ROC-AUC", f"{metrics['rocAuc']:.3f}"),
    ("Référés", str(metrics["referred"])),
]
for col, (label, value) in zip(cols, kpis):
    with col:
        kpi_card(label, value) 
        """
Dashboard Responsable de structure (cf. cahier des charges §5).
KPIs, performance du modèle, SHAP global, évolution temporelle, historique complet.
"""

import pandas as pd
import streamlit as st

from utils.auth import is_authenticated, login_page, logout, current_display_name
from utils.components import load_css, card_start, card_end, kpi_card, app_header, error_banner
from utils.api_client import get_metrics, get_history, ApiError
from utils.plotting import (
    apply_theme, risk_distribution_chart, roc_curve_chart,
    confusion_matrix_chart, shap_global_chart, timeline_chart,
)

st.set_page_config(page_title="AI Credit Risk — Dashboard", page_icon="📊", layout="wide")
load_css()

# --- Authentification (§6.3 : rôle RESPONSABLE requis) ---
if not is_authenticated():
    login_page(expected_role="RESPONSABLE")
    st.stop()

if st.session_state.get("role") != "RESPONSABLE":
    error_banner("Ce compte n'a pas accès au dashboard Responsable.")
    st.stop()

# --- En-tête ---
header_col, logout_col = st.columns([9, 1])
with header_col:
    app_header(current_display_name(), "Dashboard Responsable de structure")
with logout_col:
    if st.button("Déconnexion", use_container_width=True):
        logout()

st.markdown("<br>", unsafe_allow_html=True)

try:
    metrics = get_metrics()
except ApiError as e:
    error_banner(str(e))
    st.stop()

# --- KPIs (§5.3) ---
kpi_cols = st.columns(5)
kpis = [
    ("Demandes totales", f"{metrics['total']:,}".replace(",", " "), "📄"),
    ("Taux de défaut moyen", f"{metrics['avg_default']*100:.1f}%", "📉"),
    ("Proportion HIGH", f"{metrics['pct_high']*100:.1f}%", "🔴"),
    ("Performance ROC-AUC", f"{metrics['rocAuc']:.3f}", "🎯"),
    ("Dossiers référés", f"{metrics['referred']:,}".replace(",", " "), "🔁"),
]
for col, (label, value, icon) in zip(kpi_cols, kpis):
    with col:
        kpi_card(label, value, icon)

st.markdown("<br>", unsafe_allow_html=True)

# --- Graphiques (§5.4) ---
row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    card_start("Répartition des risques")
    dist = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
    for row in get_history(full=True, limit=200):
        dist[row["riskCategory"]] = dist.get(row["riskCategory"], 0) + 1
    st.plotly_chart(risk_distribution_chart(dist), use_container_width=True)
    card_end()

with row1_col2:
    card_start("Performance du modèle")
    st.plotly_chart(apply_theme(roc_curve_chart(metrics["rocAuc"])), use_container_width=True)
    card_end()

row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    card_start("Matrice de confusion")
    st.plotly_chart(confusion_matrix_chart(metrics["confusionMatrix"]), use_container_width=True)
    card_end()

with row2_col2:
    card_start("SHAP global — Top 10 variables")
    st.plotly_chart(shap_global_chart(metrics["shapGlobal"]), use_container_width=True)
    card_end()

card_start("Évolution temporelle du taux de défaut")
st.plotly_chart(timeline_chart(metrics["timeline"]), use_container_width=True)
card_end()

# --- Historique complet (§5.2 point 4) ---
card_start("Historique complet des prédictions")
try:
    history = get_history(full=True, limit=100)
    df = pd.DataFrame(history)
    st.dataframe(df, use_container_width=True, hide_index=True)
except ApiError as e:
    error_banner(str(e))
card_end()
