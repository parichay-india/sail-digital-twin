"""
═══════════════════════════════════════════════════════════════════════════════
 SAIL Digital Twin — Page 3: Model Card & Accuracy
═══════════════════════════════════════════════════════════════════════════════
 Transparent explanation of how the AI model was built, what data it learned
 from, what features it uses, and proof of >98% prediction accuracy.
 Designed for Jury members who want to understand the engineering behind
 the numbers — no black-box claims.
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.styling import (
    apply_custom_theme, render_header, render_kpi_card,
    render_section_divider, SAIL_NAVY, SAIL_RED, SAIL_GREEN, SAIL_GOLD,
)
from utils.data_loader import (
    load_performance_report,
    load_feature_metadata, load_target_metadata,
    load_feature_cols, load_target_cols,
)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE SETUP
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(page_title="Model Card | SAIL", page_icon="🎓", layout="wide")
apply_custom_theme()

render_header(
    title="🎓 Model Card & Accuracy Validation",
    subtitle="Transparent engineering — how the AI was built, what it learned, how it validates.",
    context="This page exists so no jury member ever has to take a performance claim on faith."
)

report = load_performance_report()
feature_meta = load_feature_metadata()
target_meta  = load_target_metadata()
feature_cols = load_feature_cols()
target_cols  = load_target_cols()


if not report:
    st.warning("Performance report not available. Please run the Jupyter notebook first.")
    st.stop()


# ═══════════════════════════════════════════════════════════════════════════════
# HEADLINE MODEL METRICS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("### 🏆 Headline Model Performance (5-Fold Cross-Validation)")

cv_acc  = report.get('cv_accuracy_mean', 0)
cv_std  = report.get('cv_accuracy_std', 0)
cv_r2   = report.get('cv_r2_mean', 0)
cv_mae  = report.get('cv_mae_mean', 0)

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Prediction Accuracy",
                    f"{cv_acc:.2f}%",
                    f"±{cv_std:.2f}% across 5 folds",
                    color=SAIL_GREEN if cv_acc >= 98 else SAIL_GOLD,
                    icon="✅")
with c2:
    render_kpi_card("R² Score",
                    f"{cv_r2:.4f}",
                    "Coefficient of determination",
                    color=SAIL_NAVY, icon="📈")
with c3:
    render_kpi_card("Mean Absolute Error",
                    f"{cv_mae:.2f} °C",
                    "Zone setpoint prediction",
                    color=SAIL_NAVY, icon="🎯")
with c4:
    render_kpi_card("Training Samples",
                    f"{report.get('training_samples', 0):,}",
                    f"Held-out: {report.get('test_samples', 0):,} rows",
                    color=SAIL_NAVY, icon="📚")


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════════
render_section_divider()

tab_arch, tab_features, tab_validation, tab_equation = st.tabs([
    "🏗️ Architecture", "🔍 Features", "🧪 Validation", "📐 The Equation"
])


with tab_arch:
    st.markdown("### Model Architecture Overview")
    c1, c2 = st.columns([1.3, 1])

    with c1:
        st.markdown("""
        #### The Dual-Model Ensemble

        We deliberately train **two complementary models** and average their predictions.
        This gives us both **interpretability** and **performance** in one system.

        ##### 📐 Model A — Multivariate Polynomial Regression (MVPR)
        - **Algorithm:** Polynomial features (degree 2) + Ridge regression
        - **Strength:** Fully interpretable — each coefficient is a physical relationship the operator can read
        - **Regularization:** Ridge (α=1.0) prevents overfitting on interaction terms
        - **This is the equation shown in our project report and patents**

        ##### 🌲 Model B — XGBoost Gradient Boosting
        - **Algorithm:** 400 boosted regression trees · Max depth 6 · Learning rate 0.05
        - **Strength:** Captures non-linear interactions that polynomials cannot
        - **Regularization:** α=0.1 (L1) + λ=1.0 (L2) + min_child_weight=10
        - **Validated:** 5-fold cross-validation to detect overfitting

        ##### 🤝 Ensemble
        Final predictions are the **average of MVPR and XGBoost** outputs. This gives us:
        - ✅ Interpretability retained (operators can still read the polynomial)
        - ✅ Higher accuracy than either model alone
        - ✅ Robustness to individual model failure modes
        """)

    with c2:
        # Architecture diagram (simple vertical flow)
        arch_fig = go.Figure()

        boxes = [
            ("Raw Sensor Data\n(15+ variables every 5 min)", 0.5, 0.90, "#ECEFF4"),
            ("StandardScaler\n(normalize inputs)", 0.5, 0.72, "#D8DEE9"),
            ("MVPR\n(Poly degree 2 + Ridge)", 0.2, 0.48, "#1F3864"),
            ("XGBoost\n(400 trees · depth 6)", 0.8, 0.48, "#C00000"),
            ("Ensemble Average", 0.5, 0.26, "#2E7D7D"),
            ("Predicted Setpoints\n(RTH · RTS · RJC · Snout)", 0.5, 0.08, "#00B050"),
        ]

        for text, x, y, color in boxes:
            is_dark = color in ["#1F3864", "#C00000", "#2E7D7D", "#00B050"]
            text_color = 'white' if is_dark else '#1A1A1A'
            arch_fig.add_annotation(
                x=x, y=y, text=text,
                showarrow=False,
                font=dict(size=11, color=text_color, family='Segoe UI'),
                bgcolor=color, bordercolor='white', borderwidth=2,
                width=180, height=50,
            )

        # Arrows
        arrows = [
            (0.5, 0.86, 0.5, 0.76),
            (0.5, 0.68, 0.25, 0.54),
            (0.5, 0.68, 0.75, 0.54),
            (0.25, 0.44, 0.48, 0.30),
            (0.75, 0.44, 0.52, 0.30),
            (0.5, 0.22, 0.5, 0.12),
        ]
        for ax, ay, x, y in arrows:
            arch_fig.add_annotation(
                x=x, y=y, ax=ax, ay=ay,
                xref='x', yref='y', axref='x', ayref='y',
                showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=1.5,
                arrowcolor='#595959'
            )

        arch_fig.update_layout(
            xaxis=dict(visible=False, range=[0, 1]),
            yaxis=dict(visible=False, range=[0, 1]),
            height=520, plot_bgcolor='#FAFAFA', paper_bgcolor='white',
            margin=dict(l=10, r=10, t=20, b=10), showlegend=False,
        )
        st.plotly_chart(arch_fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: Features
# ─────────────────────────────────────────────────────────────────────────────
with tab_features:
    st.markdown("### Input Features & Their Relative Importance")
    st.caption("The AI looks at 10 process variables. Here's how much each one influences the primary prediction (RTH strip setpoint).")

    # Feature importance chart
    fi = report.get('feature_importance', {})
    if fi:
        fi_df = pd.DataFrame([
            {'Feature': feature_meta.get(f, {}).get('label', f),
             'Internal Name': f,
             'Importance': imp,
             'Unit': feature_meta.get(f, {}).get('unit', '—')}
            for f, imp in fi.items()
        ]).sort_values('Importance', ascending=True)

        fi_fig = go.Figure()
        fi_fig.add_trace(go.Bar(
            y=fi_df['Feature'], x=fi_df['Importance'],
            orientation='h',
            marker=dict(
                color=fi_df['Importance'],
                colorscale=[[0, '#D8DEE9'], [1, SAIL_NAVY]],
                line=dict(width=0)
            ),
            text=[f"{v:.3f}" for v in fi_df['Importance']],
            textposition='outside',
            hovertemplate="<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>",
        ))
        fi_fig.update_layout(
            title="Feature Importance — Primary Target (rthstrip_SP)",
            xaxis_title="Relative Importance",
            height=440, plot_bgcolor='white',
            margin=dict(l=180, r=40, t=50, b=40),
        )
        st.plotly_chart(fi_fig, use_container_width=True)

    # Feature description table
    st.markdown("#### Feature Dictionary")
    desc_rows = [
        {'Feature': feature_meta[f]['label'],
         'Internal': f, 'Unit': feature_meta[f]['unit'],
         'Typical Range': f"{feature_meta[f]['min']:.2f} – {feature_meta[f]['max']:.2f}",
         'Description': feature_meta[f]['description']}
        for f in feature_cols
    ]
    st.dataframe(pd.DataFrame(desc_rows), hide_index=True, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: Validation (test-set metrics)
# ─────────────────────────────────────────────────────────────────────────────
with tab_validation:
    st.markdown("### Held-Out Test Set Performance")
    st.caption("Model performance on data the model **never saw during training**. This is the only honest accuracy claim.")

    metrics = report.get('test_metrics', [])
    if metrics:
        m_df = pd.DataFrame(metrics)

        # Filter to ensemble only for the main table
        ens_df = m_df[m_df['Model'] == 'Ensemble'].copy()
        ens_df['Target'] = ens_df['Target'].map(lambda t: target_meta.get(t, {}).get('label', t))

        st.markdown("#### Ensemble Performance (per target zone)")
        st.dataframe(ens_df.drop(columns=['Model']), hide_index=True, use_container_width=True)

        # Compare all 3 models
        st.markdown("#### Model Comparison (all 3 variants)")
        comp = m_df.pivot_table(
            index='Target', columns='Model',
            values=['R²', 'MAE (°C)', 'Accuracy (%)']
        ).round(3)
        st.dataframe(comp, use_container_width=True)

        # Bar chart: accuracy per target
        avg_acc = m_df.groupby('Model')['Accuracy (%)'].mean().reset_index()
        acc_fig = go.Figure()
        acc_fig.add_trace(go.Bar(
            x=avg_acc['Model'], y=avg_acc['Accuracy (%)'],
            marker=dict(
                color=[SAIL_GREEN if v >= 98 else SAIL_GOLD for v in avg_acc['Accuracy (%)']],
                line=dict(width=0)
            ),
            text=[f"{v:.2f}%" for v in avg_acc['Accuracy (%)']],
            textposition='outside',
        ))
        acc_fig.add_hline(y=98, line_dash='dash', line_color=SAIL_RED,
                          annotation_text="98% accuracy target", annotation_position="top right")
        acc_fig.update_layout(
            title="Accuracy by Model (Averaged Across 4 Target Zones)",
            yaxis=dict(title="Accuracy (%)", range=[90, 101], gridcolor='#E8E8E8'),
            height=420, plot_bgcolor='white',
        )
        st.plotly_chart(acc_fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4: The Equation (interpretability)
# ─────────────────────────────────────────────────────────────────────────────
with tab_equation:
    st.markdown("### The Explicit Equation")
    st.caption("The MVPR branch of the model produces an equation that can be written on a whiteboard. No magic.")

    st.latex(r"""
    Y_{\text{zone}} = c_1 + \sum_{i=1}^{n} a_i \cdot x_i
                    + \sum_{i \leq j} b_{ij} \cdot x_i \cdot x_j + c_2
    """)

    st.markdown(r"""
    Where:
    - $Y_{\text{zone}}$ = predicted optimal setpoint for a given furnace zone (°C)
    - $x_i \in \{$ thickness, width, linespeed, pottemp, VIP11, VIP12, DFF exit, POR, enloop, exloop $\}$
    - $a_i$ = linear coefficients (what each feature contributes on its own)
    - $b_{ij}$ = interaction coefficients (e.g., thickness × speed captures how thin fast strips need different setpoints)
    - $c_1, c_2$ = bias terms
    """)

    st.markdown("#### Why this matters to a plant operator")
    st.info("""
    A plant operator can read this equation and understand **exactly why** the AI recommends a setpoint.
    For a thin, wide, fast coil, they can see in the equation:

    - Linear terms drive the baseline
    - Interaction term `thickness × linespeed` boosts setpoint when the strip is thin AND moving fast
    (compensating for reduced residence time in the furnace)

    **No black box. No vendor magic. An equation any engineer at the plant can critique and trust.**
    """)

    st.markdown("---")
    st.markdown("#### Governance & Re-training")
    st.markdown("""
    - **Quarterly re-training:** Every 3 months, the coefficients are re-fit on the latest operational data
    - **Version controlled:** Every trained model is tagged (v1.0, v1.1 …) and logged with validation metrics
    - **Human in the loop:** Plant operators can always override the AI's suggested setpoint via the PLC/SCADA
    - **Audit trail:** Every inference is logged — input vector, predicted setpoint, operator override (if any)
    """)
