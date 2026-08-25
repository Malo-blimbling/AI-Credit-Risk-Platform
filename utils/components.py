"""
Composants UI réutilisables (cartes "glass", badges, gauge de risque, KPI cards).
Tous les fichiers qui les utilisent doivent `import streamlit as st` eux-mêmes.
"""

import os
import streamlit as st

from utils.config import COLORS, RISK_LABELS, RISK_ICONS


def load_css():
    """Charge assets/style.css dans la page. À appeler une fois en tête de chaque app."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def card_start(title: str = None):
    if title:
        st.markdown(f'<div class="glass-card"><h3>{title}</h3>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)


def card_end():
    st.markdown('</div>', unsafe_allow_html=True)


def risk_badge(category: str) -> str:
    css_class = category.lower()
    icon = RISK_ICONS.get(category, "")
    label = RISK_LABELS.get(category, category)
    return f'<span class="risk-badge {css_class}">{icon} {category} — {label}</span>'


def risk_gauge(score: int, category: str):
    css_class = category.lower()
    score = max(0, min(100, int(score)))
    st.markdown(
        f"""
        <div class="risk-gauge {css_class}" style="--pct:{score};">
            <div style="text-align:center;">
                <div class="value mono-number">{score}</div>
                <div class="label">/ 100</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, icon: str = ""):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-value">{icon} {value}</div>
            <div class="kpi-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def app_header(display_name: str, role_label: str):
    """En-tête commun : logo, nom de l'utilisateur, bouton déconnexion (cf. §4.2 / §5.2)."""
    col1, col2, col3 = st.columns([3, 5, 1.4])
    with col1:
        st.markdown(
            f'<div class="app-title" style="font-size:1.3rem;">AI Credit Risk</div>'
            f'<div style="color:var(--text-secondary); font-size:.8rem;">{role_label}</div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.write("")
    with col3:
        st.markdown(f'<div style="text-align:right; padding-top:.4rem;">{display_name}</div>', unsafe_allow_html=True)


def error_banner(message: str):
    st.markdown(
        f'<div class="glass-card" style="border-left:4px solid {COLORS["high"]};">⚠️ {message}</div>',
        unsafe_allow_html=True,
    )
