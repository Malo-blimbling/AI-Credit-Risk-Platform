"""
Thème Plotly commun + constructeurs de graphiques (cf. cahier des charges §5.4).
"""

import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from utils.config import COLORS


def apply_theme(fig: go.Figure, title: str = None) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        font=dict(family="Inter, sans-serif", color="#0F1F33", size=13),
        title=dict(
            text=title,
            font=dict(family="Space Grotesk, sans-serif", size=16, color=COLORS["primary_dark"]),
        ) if title else None,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=20, t=50 if title else 20, b=30),
        colorway=[COLORS["primary"], COLORS["primary_light"], COLORS["medium"], COLORS["high"]],
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=False, linecolor="#DCE4EE")
    fig.update_yaxes(showgrid=True, gridcolor="#EEF2F7", zeroline=False)
    return fig


def shap_bar_chart(shap_values: dict, title: str = None) -> go.Figure:
    items = sorted(shap_values.items(), key=lambda kv: abs(kv[1]))
    names = [k for k, _ in items]
    values = [v for _, v in items]
    colors = [COLORS["high"] if v > 0 else COLORS["low"] for v in values]
    fig = go.Figure(go.Bar(x=values, y=names, orientation="h", marker_color=colors))
    return apply_theme(fig, title)


def risk_distribution_chart(counts: dict) -> go.Figure:
    labels = list(counts.keys())
    values = list(counts.values())
    colors = [COLORS.get(l.lower(), COLORS["primary"]) for l in labels]
    fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.55, marker=dict(colors=colors)))
    return apply_theme(fig, "Répartition des risques")


def roc_curve_chart(roc_auc: float) -> go.Figure:
    # Courbe indicative reconstituée à partir de l'AUC (le backend peut fournir
    # les points fpr/tpr réels via un endpoint dédié si besoin).
    fpr = np.linspace(0, 1, 50)
    tpr = fpr ** (1 / max(roc_auc, 0.5) - 1) if roc_auc > 0.5 else fpr
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name=f"ROC (AUC={roc_auc:.3f})",
                              line=dict(color=COLORS["primary"], width=3)))
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Aléatoire",
                              line=dict(color="#C4CDD9", dash="dash")))
    return apply_theme(fig, "Courbe ROC")


def confusion_matrix_chart(matrix: list) -> go.Figure:
    labels = ["Pas de défaut", "Défaut"]
    fig = go.Figure(go.Heatmap(
        z=matrix, x=labels, y=labels,
        colorscale=[[0, "#EAF1FA"], [1, COLORS["primary"]]],
        showscale=False,
        text=matrix, texttemplate="%{text}",
    ))
    fig.update_yaxes(autorange="reversed")
    return apply_theme(fig, "Matrice de confusion")


def shap_global_chart(shap_global: dict) -> go.Figure:
    items = sorted(shap_global.items(), key=lambda kv: kv[1])[-10:]
    names = [k for k, _ in items]
    values = [v for _, v in items]
    fig = go.Figure(go.Bar(x=values, y=names, orientation="h", marker_color=COLORS["primary"]))
    return apply_theme(fig, "Top 10 variables (SHAP global)")


def timeline_chart(timeline: list) -> go.Figure:
    periods = [p["period"] for p in timeline]
    values = [p["avg_default"] for p in timeline]
    fig = go.Figure(go.Scatter(x=periods, y=values, mode="lines+markers",
                                line=dict(color=COLORS["primary"], width=3),
                                marker=dict(size=6)))
    return apply_theme(fig, "Évolution du taux de défaut moyen")
