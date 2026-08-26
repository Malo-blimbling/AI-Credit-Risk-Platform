"""Authentification Basic HTTP et gestion de session frontend."""

import streamlit as st
import requests

from utils.config import API_BASE_URL, ENDPOINTS, API_TIMEOUT
from utils.components import load_css


def check_credentials(username: str, password: str):
    """Retourne (ok: bool, role: str|None, display_name: str|None)."""
    try:
        resp = requests.get(
            f"{API_BASE_URL}{ENDPOINTS['health']}",
            auth=(username, password),
            timeout=API_TIMEOUT,
        )
        if resp.status_code == 200:
            # Le rôle doit être déduit de la réponse API si elle l'expose,
            # sinon adapter selon le contrat réel du backend.
            role = resp.headers.get("X-User-Role", "AGENT")
            return True, role, username
        return False, None, None
    except requests.exceptions.ConnectionError:
        st.session_state["_auth_error"] = "Service temporairement indisponible."
        return False, None, None


def is_authenticated() -> bool:
    return st.session_state.get("authenticated", False)


def current_role() -> str:
    return st.session_state.get("role", "")


def current_display_name() -> str:
    return st.session_state.get("display_name", "")


def logout():
    for key in ("authenticated", "role", "display_name", "username", "credentials", "last_result"):
        st.session_state.pop(key, None)
    st.rerun()


def login_page(expected_role: str = None):
    """Affiche la page de connexion. Si expected_role est fourni, refuse les
    utilisateurs authentifiés dont le rôle ne correspond pas à cette app."""
    load_css()

    st.markdown(
        """
        <div style="position:fixed; inset:0; z-index:-1;
            background: linear-gradient(135deg, #0B1F3A 0%, #00529B 55%, #1B6FB8 100%);"></div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="app-title" style="font-size:1.5rem; margin-bottom:0;">AI Credit Risk</div>'
        '<p style="color:var(--text-secondary); margin-top:2px; margin-bottom:1.5rem;">'
        'Plateforme de prédiction du risque de crédit</p>',
        unsafe_allow_html=True,
    )

    if st.session_state.get("_auth_error"):
        st.error(st.session_state.pop("_auth_error"))

    with st.form("login_form"):
        username = st.text_input("Identifiant")
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter", use_container_width=True)

    if submitted:
        ok, role, display_name = check_credentials(username, password)
        if ok and (expected_role is None or role == expected_role):
            st.session_state["authenticated"] = True
            st.session_state["role"] = role
            st.session_state["display_name"] = display_name
            st.session_state["username"] = username
            st.session_state["credentials"] = (username, password)
            st.rerun()
        elif ok:
            st.error("Ce compte n'a pas accès à cette interface.")
        else:
            st.error("Identifiant ou mot de passe incorrect.")

    st.markdown('</div></div>', unsafe_allow_html=True)
