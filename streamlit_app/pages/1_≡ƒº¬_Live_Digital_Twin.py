"""
═══════════════════════════════════════════════════════════════════════════════
 SAIL Digital Twin — Page 1: Live Digital Twin
═══════════════════════════════════════════════════════════════════════════════
 The interactive heart of the dashboard. The Jury (or any user) can adjust
 process inputs with sliders and watch the AI predict optimal zone setpoints
 in real time. Visually demonstrates what the production model does every
 5 minutes on the Bokaro galvanizing line.
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.styling import (
    apply_custom_theme, render_header, render_kpi_card,
    render_section_divider, SAIL_NAVY, SAIL_RED, SAIL_GREEN
)
from utils.data_loader import (
    check_artifacts_present,
    load_feature_metadata, load_target_metadata,
    load_feature_cols, load_target_cols,
    predict_setpoints
)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE SETUP
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(page_title="Live Digital Twin | SAIL", page_icon="🧪", layout="wide")
apply_custom_theme()

ok, missing = check_artifacts_present()
if not ok:
    st.error("⚠️ Model artifacts missing. Please run the Jupyter notebook first.")
    st.stop()

render_header(
    title="🧪 Live Digital Twin",
    subtitle="Adjust process variables on the left — the AI engine predicts optimal zone setpoints in real time.",
    context="This is a visual replica of what the AI does every 5 minutes on the Bokaro galvanizing line."
)

# Load metadata
feature_meta = load_feature_metadata()
target_meta  = load_target_metadata()
feature_cols = load_feature_cols()
target_cols  = load_target_cols()


# ═══════════════════════════════════════════════════════════════════════════════
# SCENARIO PRESETS (for one-click demos)
# ═══════════════════════════════════════════════════════════════════════════════
SCENARIOS = {
    "⚙️ Standard Production (Default)": {f: feature_meta[f]['default'] for f in feature_cols},
    "📏 Thin-Gauge Strip (<0.6mm)": {
        'coilthickness': 0.45, 'coilwidth': 1100, 'linespeed': 100,
        'pottemp': 460, 'vip11power': 280, 'vip12power': 280,
        'dffstrip_ACT': 480, 'porrest': 80, 'enloop': 75, 'exloop': 40,
    },
    "📐 Wide Heavy Strip (>1350mm)": {
        'coilthickness': 1.6, 'coilwidth': 1400, 'linespeed': 75,
        'pottemp': 460, 'vip11power': 380, 'vip12power': 380,
        'dffstrip_ACT': 510, 'porrest': 120, 'enloop': 78, 'exloop': 38,
    },
    "🏃 High-Speed Medium Gauge": {
        'coilthickness': 0.8, 'coilwidth': 1200, 'linespeed': 110,
        'pottemp': 460, 'vip11power': 320, 'vip12power': 320,
        'dffstrip_ACT': 495, 'porrest': 100, 'enloop': 77, 'exloop': 42,
    },
    "🧪 Transient State (Coil Transition)": {
        'coilthickness': 0.55, 'coilwidth': 1010, 'linespeed': 65,
        'pottemp': 459, 'vip11power': 250, 'vip12power': 250,
        'dffstrip_ACT': 470, 'porrest': 30, 'enloop': 70, 'exloop': 35,
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — SCENARIO + MODEL CONTROLS
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🎬 Scenario Presets")
    st.caption("Jump to a pre-configured operational scenario, or adjust inputs manually below.")

    scenario_name = st.selectbox(
        "Load preset:",
        options=list(SCENARIOS.keys()),
        index=0,
        help="Each preset loads a typical operating condition from the plant."
    )

    if 'active_scenario' not in st.session_state or st.session_state.active_scenario != scenario_name:
        st.session_state.active_scenario = scenario_name
        for k, v in SCENARIOS[scenario_name].items():
            st.session_state[f'input_{k}'] = v

    st.markdown("---")
    st.markdown("### 🧠 Inference Engine")
    model_type = st.radio(
        "Prediction model:",
        ["ensemble", "xgboost", "mvpr"],
        format_func=lambda x: {
            "ensemble": "🤝 Ensemble (XGBoost + MVPR)",
            "xgboost": "🌲 XGBoost Only",
            "mvpr": "📐 MVPR Only (interpretable)"
        }[x],
        index=0,
        help="Ensemble = both models averaged (highest accuracy). MVPR = pure polynomial regression (interpretable equation)."
    )


# ═══════════════════════════════════════════════════════════════════════════════
# INPUT PANEL — SLIDERS FOR EACH FEATURE
# ═══════════════════════════════════════════════════════════════════════════════
render_section_divider("📥 Process Inputs — Real-Time Furnace State")

input_col1, input_col2 = st.columns(2)

# Split features into two logical groups for visual balance
geometry_features = ['coilthickness', 'coilwidth', 'linespeed', 'dffstrip_ACT']
thermal_features  = ['pottemp', 'vip11power', 'vip12power', 'porrest', 'enloop', 'exloop']

inputs = {}

with input_col1:
    st.markdown("**Coil Geometry & Line Dynamics**")
    for feat in geometry_features:
        if feat not in feature_meta:
            continue
        m = feature_meta[feat]
        default = st.session_state.get(f'input_{feat}', m['default'])
        inputs[feat] = st.slider(
            label=f"{m['label']} ({m['unit']})",
            min_value=float(m['min']),
            max_value=float(m['max']),
            value=float(default),
            step=(m['max'] - m['min']) / 200,
            help=m['description'],
            key=f'slider_{feat}'
        )

with input_col2:
    st.markdown("**Thermal State & Auxiliaries**")
    for feat in thermal_features:
        if feat not in feature_meta:
            continue
        m = feature_meta[feat]
        default = st.session_state.get(f'input_{feat}', m['default'])
        inputs[feat] = st.slider(
            label=f"{m['label']} ({m['unit']})",
            min_value=float(m['min']),
            max_value=float(m['max']),
            value=float(default),
            step=(m['max'] - m['min']) / 200,
            help=m['description'],
            key=f'slider_{feat}'
        )


# ═══════════════════════════════════════════════════════════════════════════════
# RUN INFERENCE
# ═══════════════════════════════════════════════════════════════════════════════
with st.spinner("🧠 AI inference..."):
    predictions = predict_setpoints(inputs, model_type=model_type)


# ═══════════════════════════════════════════════════════════════════════════════
# DERIVED ANALYTICS — ZONE SELECTION LOGIC (from Intervention 1)
# ═══════════════════════════════════════════════════════════════════════════════
width = inputs['coilwidth']
if width <= 1050:
    zone_config = "Centre Zone Only"
    n_burners = 48
    zone_color = SAIL_NAVY
elif width <= 1350:
    zone_config = "Centre + Medium Zones"
    n_burners = 64
    zone_color = "#E67E22"
else:
    zone_config = "All Three Zones (Centre + Medium + Wide)"
    n_burners = 80
    zone_color = SAIL_RED

# Thin-gauge Lean Firing check (Intervention 4)
thin_gauge = inputs['coilthickness'] < 0.6
lean_firing_active = thin_gauge


# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT PANEL — PREDICTED SETPOINTS
# ═══════════════════════════════════════════════════════════════════════════════
render_section_divider("🎯 AI Predictions — Optimal Zone Setpoints")

pred_cols = st.columns(len(target_cols))
for i, t in enumerate(target_cols):
    with pred_cols[i]:
        meta = target_meta[t]
        render_kpi_card(
            label=meta['label'],
            value=f"{predictions[t]:.1f} {meta['unit']}",
            delta=meta['description'][:50] + "..." if len(meta['description']) > 50 else meta['description'],
            color=SAIL_NAVY,
            icon="🔥"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# BURNER ZONING VISUALIZATION
# ═══════════════════════════════════════════════════════════════════════════════
render_section_divider("🔥 Burner Zoning Decision (Intervention 1)")

col_a, col_b = st.columns([1, 2])

with col_a:
    st.markdown(f"""
    <div style='background-color:{zone_color}15; border-left:5px solid {zone_color};
                padding:18px; border-radius:10px;'>
        <h4 style='margin-top:0; color:{zone_color};'>Active Zone Configuration</h4>
        <p style='font-size:1.25em; font-weight:700; color:{zone_color}; margin: 6px 0;'>
            {zone_config}
        </p>
        <p style='margin: 6px 0;'><b>Burners Fired:</b> {n_burners} / 80</p>
        <p style='margin: 6px 0;'><b>Trigger:</b> Strip width = {width:.0f}mm</p>
    </div>
    """, unsafe_allow_html=True)

    if lean_firing_active:
        st.markdown(f"""
        <div style='background-color:#FFF4E6; border-left:5px solid #F39C12;
                    padding:14px; border-radius:8px; margin-top:12px;'>
            <b style='color:#E67E22;'>⚠️ Lean Firing Mode ACTIVE</b><br>
            <span style='font-size:0.9em;'>
                Thickness {inputs['coilthickness']:.2f}mm &lt; 0.6mm threshold.<br>
                AI pre-emptively staggers firing to prevent heat buckling.
            </span>
        </div>
        """, unsafe_allow_html=True)

with col_b:
    # Visual: burner grid showing which zones are firing
    burner_fig = go.Figure()

    # Build a burner matrix for visualization
    # 80 burners arranged: 8 rows × 10 columns
    # Centre (cols 3-7, all rows) = 48; Medium (cols 1-2, 8-9) = 16; Wide (cols 0, 9) — adjust for 16
    burner_positions = []
    burner_zones = []
    burner_active = []
    for row in range(8):
        for col in range(10):
            burner_positions.append((col, row))
            # Classify by column (lateral position)
            if 3 <= col <= 7:
                zone = 'Centre'
            elif col in [2, 8]:
                zone = 'Medium'
            else:  # cols 0, 1, 9
                zone = 'Wide'
            burner_zones.append(zone)
            # Activate based on strip width logic
            if zone == 'Centre':
                active = True  # Always on
            elif zone == 'Medium':
                active = width > 1050
            else:
                active = width > 1350
            burner_active.append(active)

    xs = [p[0] for p in burner_positions]
    ys = [p[1] for p in burner_positions]
    colors = []
    symbols = []
    for z, a in zip(burner_zones, burner_active):
        if not a:
            colors.append('lightgrey')
        elif z == 'Centre':
            colors.append(SAIL_NAVY)
        elif z == 'Medium':
            colors.append('#E67E22')
        else:
            colors.append(SAIL_RED)
        symbols.append('square')

    burner_fig.add_trace(go.Scatter(
        x=xs, y=ys,
        mode='markers',
        marker=dict(size=22, color=colors, symbol=symbols,
                    line=dict(width=1, color='white')),
        hovertemplate='Zone: %{text}<extra></extra>',
        text=burner_zones,
        showlegend=False
    ))

    # Legend boxes
    for label, color in [("Centre (48)", SAIL_NAVY),
                         ("Medium (16)", '#E67E22'),
                         ("Wide (16)", SAIL_RED),
                         ("Inactive", 'lightgrey')]:
        burner_fig.add_trace(go.Scatter(
            x=[None], y=[None], mode='markers',
            marker=dict(size=14, color=color, symbol='square'),
            name=label, showlegend=True
        ))

    burner_fig.update_layout(
        title=f"DFF-4 Burner Panel · {n_burners} / 80 Active",
        xaxis=dict(visible=False, range=[-0.8, 9.8]),
        yaxis=dict(visible=False, range=[-0.5, 7.5], scaleanchor='x'),
        height=340,
        margin=dict(l=10, r=10, t=45, b=10),
        plot_bgcolor='#F9F9F9',
        paper_bgcolor='white',
        legend=dict(orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5)
    )
    st.plotly_chart(burner_fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# FURNACE THERMAL PROFILE VISUALIZATION
# ═══════════════════════════════════════════════════════════════════════════════
render_section_divider("🌡️ Predicted Furnace Thermal Profile")

# Build a line chart showing how the strip heats through the furnace zones
profile_zones = ['DFF Exit', 'RTH Zone', 'RTS Zone', 'RJC']
profile_values = [
    inputs['dffstrip_ACT'],
    predictions['rthstrip_SP'],
    predictions['rtsstrip_SP'],
    target_meta['rtszone_SP']['mean'] * 0.88,  # approx RJC via coolant
]

profile_fig = go.Figure()
profile_fig.add_trace(go.Scatter(
    x=profile_zones,
    y=profile_values,
    mode='lines+markers+text',
    line=dict(color=SAIL_RED, width=4),
    marker=dict(size=16, color=SAIL_RED, line=dict(color='white', width=2)),
    text=[f"{v:.0f}°C" for v in profile_values],
    textposition="top center",
    textfont=dict(size=13, color=SAIL_NAVY, family='Segoe UI'),
    name='Strip Temperature',
    fill='tozeroy',
    fillcolor='rgba(192, 0, 0, 0.08)',
))

profile_fig.update_layout(
    title="Strip Temperature as It Travels Through the Furnace",
    xaxis_title="Furnace Zone (strip travel direction →)",
    yaxis_title="Temperature (°C)",
    height=380,
    plot_bgcolor='white',
    margin=dict(l=40, r=20, t=60, b=60),
    showlegend=False,
    yaxis=dict(gridcolor='#E8E8E8'),
)
st.plotly_chart(profile_fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# INPUT VECTOR SUMMARY (audit trail)
# ═══════════════════════════════════════════════════════════════════════════════
with st.expander("🔍 Show raw input vector sent to the model (audit trail)", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Input Features (what the AI receives)**")
        inp_df = pd.DataFrame([
            {'Feature': feature_meta[f]['label'],
             'Unit': feature_meta[f]['unit'],
             'Value': round(inputs[f], 3)}
            for f in feature_cols
        ])
        st.dataframe(inp_df, hide_index=True, use_container_width=True)
    with c2:
        st.markdown("**Output Predictions (what the AI returns)**")
        out_df = pd.DataFrame([
            {'Target': target_meta[t]['label'],
             'Unit': target_meta[t]['unit'],
             'Predicted': round(predictions[t], 2)}
            for t in target_cols
        ])
        st.dataframe(out_df, hide_index=True, use_container_width=True)

    st.caption(f"Inference engine: **{model_type}** · Model v1.0 · "
               "All computations run on-premise with no external network calls.")


# ═══════════════════════════════════════════════════════════════════════════════
# EDUCATIONAL NOTE
# ═══════════════════════════════════════════════════════════════════════════════
st.info("""
💡 **How to interpret this Digital Twin**

In production, the AI receives these same input signals every 5 minutes directly from the PLC/SCADA system.
It computes the optimal setpoints using the equation shown on the Model Card page, and writes them back to the
plant controllers through MQTT-bridged OPC-UA interfaces — all inside the existing ISMS 27001:2013 compliant
automation perimeter. What you just did manually with sliders, the AI does autonomously, continuously,
**over 100,000 times per year**.
""")
