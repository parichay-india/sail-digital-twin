"""
═══════════════════════════════════════════════════════════════════════════════
 SAIL DIGITAL TWIN — Home Page
 AI-Assisted Intelligent Stoichiometric Optimization
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from utils.styling import apply_custom_theme, render_header, render_kpi_card
from utils.data_loader import load_performance_report, check_artifacts_present, load_kpi_summary, get_path_info


st.set_page_config(
    page_title="SAIL Digital Twin | DFF Stoichiometric AI",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': """
        **SAIL Digital Twin v1.1**

        AI-Assisted Intelligent Stoichiometric Optimization in DFF Section Burners

        SAIL Digital Transformation Division | ICC Technology Excellence Awards 2026
        """
    }
)

apply_custom_theme()


# Verify artifacts
artifacts_ok, missing = check_artifacts_present()
paths = get_path_info()

if not artifacts_ok:
    st.error("⚠️ **Model artifacts not found.** Please run the Jupyter notebook first.")
    st.info(f"Expected location: `{paths['model_dir']}`")
    st.info(f"Missing files: {', '.join(missing)}")
    st.markdown("""
    ### Setup Steps
    1. Open `notebooks/01_sail_digital_twin_development.ipynb` in Google Colab
    2. Mount Google Drive and upload `SAIL_Master_Dataset.xlsx` (or CSV files) to
       `MyDrive/SAIL_Digital_Twin/dataset/`
    3. Run all cells — artifacts will be saved to `MyDrive/SAIL_Digital_Twin/models/`
    4. Return here and refresh this page
    """)
    st.stop()


# Sidebar
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding: 10px 0;'>
            <h2 style='margin:0; color:#1F3864;'>🔥 SAIL</h2>
            <p style='margin:2px 0; color:#595959; font-size:0.85em;'>Digital Twin</p>
            <div style='height:2px; background:linear-gradient(90deg, #C00000 0%, #00B050 100%); margin:8px 0;'></div>
            <p style='margin:0; font-size:0.78em; color:#595959;'>
                <i>AI-Powered Furnace Intelligence</i>
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📑 Navigate")
    st.info("Use the page menu in the left sidebar to explore different views.")
    st.markdown("---")
    st.markdown("### 🏆 Recognition")
    st.success("Featured in Ministry of Steel **Chintan Shivir 2025**")
    st.caption("**Top-4** projects selected by MoS out of SAIL's 163-use-case Pravartanam programme.")
    st.markdown("---")
    st.markdown("### ⚙️ Environment")
    report = load_performance_report()
    if report:
        st.caption(f"Model v{report.get('pipeline_version', '1.1.0')}")
        st.caption(f"Trained: {report.get('training_timestamp', 'N/A')[:10]}")
    with st.expander("📁 Data paths"):
        st.caption(f"**Models:** `{paths['model_dir']}`")
        st.caption(f"**Data:** `{paths['data_dir']}`")


# Header
render_header(
    title="SAIL Digital Twin",
    subtitle="AI-Assisted Intelligent Stoichiometric Optimization in DFF Section Burners",
    context="HDGL / CRM-III, SAIL Bokaro Steel Plant  |  3-Year Transformation Journey"
)


# ═══════════════════════════════════════════════════════════════════════════════
# HERO KPIs — CUMULATIVE 2-YEAR IMPACT
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("### 📊 Two-Year Impact Dashboard — Certified Numbers")

col1, col2, col3, col4 = st.columns(4)

with col1:
    render_kpi_card(
        label="Cumulative Savings",
        value="₹8.48 Cr",
        delta="Y1: ₹3.23 Cr · Y2: ₹5.25 Cr",
        color="#C00000",
        icon="💰"
    )

with col2:
    render_kpi_card(
        label="Cumulative CO₂ Avoided",
        value="~3,930 t",
        delta="Y1: 1,500 t · Y2: 2,430 t",
        color="#00B050",
        icon="🌱"
    )

with col3:
    render_kpi_card(
        label="Propane Efficiency Gain (Y2)",
        value="26.83%",
        delta="16.644 → 12.178 kg/t",
        color="#2E74B5",
        icon="⚡"
    )

with col4:
    render_kpi_card(
        label="Project Cost",
        value="₹81,000",
        delta="Payback < 1 day · ROI > 1000×",
        color="#1F3864",
        icon="🎯"
    )


st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
# 3-PERIOD STRIP — Year-by-Year Trajectory
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("### 📅 Year-by-Year Trajectory")

kpi_df = load_kpi_summary()

if not kpi_df.empty:
    cY1, cY2, cY3 = st.columns(3)

    with cY1:
        row_a = kpi_df[kpi_df['Period'] == 'A'].iloc[0]
        st.markdown(f"""
        <div style='background-color:#FDEEEE; border-left:5px solid #C00000;
                    padding:16px; border-radius:8px; height: 200px;'>
            <h4 style='margin:0 0 4px 0; color:#C00000;'>🔻 Period A — Legacy</h4>
            <p style='margin:0; color:#595959; font-size:0.85em;'><b>{row_a['FY']}</b> (pre-AI baseline)</p>
            <hr style='margin: 8px 0; border-color: #F8D7DA;'>
            <p style='margin: 4px 0;'>Production: <b>{row_a['Production_Tons']:,.0f} T</b></p>
            <p style='margin: 4px 0;'>Propane consumed: <b>{row_a['Propane_Consumed_Tons']:,.0f} T</b></p>
            <p style='margin: 4px 0;'>Specific propane: <b>{row_a['Specific_Propane_kg_per_Ton']:.3f} kg/T</b></p>
        </div>
        """, unsafe_allow_html=True)

    with cY2:
        row_b1 = kpi_df[kpi_df['Period'] == 'B1'].iloc[0]
        st.markdown(f"""
        <div style='background-color:#E3F2FD; border-left:5px solid #2E74B5;
                    padding:16px; border-radius:8px; height: 200px;'>
            <h4 style='margin:0 0 4px 0; color:#2E74B5;'>🚀 Period B1 — AI Year 1</h4>
            <p style='margin:0; color:#595959; font-size:0.85em;'><b>{row_b1['FY']}</b> (AI deployed)</p>
            <hr style='margin: 8px 0; border-color: #BBDEFB;'>
            <p style='margin: 4px 0;'>Specific propane: <b>{row_b1['Specific_Propane_kg_per_Ton']:.3f} kg/T</b> ({row_b1['Reduction_Percent']:.2f}% ↓)</p>
            <p style='margin: 4px 0;'>Savings: <b>₹{row_b1['Financial_Saving_Cr']:.2f} Cr</b></p>
            <p style='margin: 4px 0;'>CO₂ avoided: <b>{row_b1['CO2_Avoided_Tons']:,.2f} T</b></p>
        </div>
        """, unsafe_allow_html=True)

    with cY3:
        row_b2 = kpi_df[kpi_df['Period'] == 'B2'].iloc[0]
        st.markdown(f"""
        <div style='background-color:#E8F5E9; border-left:5px solid #00B050;
                    padding:16px; border-radius:8px; height: 200px;'>
            <h4 style='margin:0 0 4px 0; color:#00B050;'>🌱 Period B2 — AI Year 2</h4>
            <p style='margin:0; color:#595959; font-size:0.85em;'><b>{row_b2['FY']}</b> (self-learning)</p>
            <hr style='margin: 8px 0; border-color: #C8E6C9;'>
            <p style='margin: 4px 0;'>Specific propane: <b>{row_b2['Specific_Propane_kg_per_Ton']:.3f} kg/T</b> ({row_b2['Reduction_Percent']:.2f}% ↓)</p>
            <p style='margin: 4px 0;'>Savings: <b>₹{row_b2['Financial_Saving_Cr']:.2f} Cr</b></p>
            <p style='margin: 4px 0;'>CO₂ avoided: <b>{row_b2['CO2_Avoided_Tons']:,.2f} T</b></p>
        </div>
        """, unsafe_allow_html=True)


st.markdown("---")


# ═══════════════════════════════════════════════════════════════════════════════
# PROJECT NARRATIVE
# ═══════════════════════════════════════════════════════════════════════════════
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### 🧭 The Journey")
    st.markdown("""
    This Digital Twin embodies the **self-learning AI engine** running inside SAIL Bokaro's
    Hot Dip Galvanizing Line. Built entirely by SAIL engineers, deployed in existing automation
    architecture, it turned a **passive, static furnace** into a **predictive, self-optimizing thermal engine**.

    #### 🔬 What the AI Does
    - Reads **10 process variables** every 5 minutes — coil geometry, line dynamics, zone temperatures, induction power
    - Predicts **optimal setpoints** for 4 furnace zones (RTH, RTS, RJC, Snout) using multivariate polynomial regression + XGBoost ensemble
    - **Retrains itself quarterly** — the longer it runs, the smarter it gets (see Year 2 accelerating savings)
    - Integrated with **Lean Firing Mode** for thin-gauge (<0.6mm) predictive coil-transition handling
    - Runs on-premise inside **ISMS 27001:2013 compliant** automation — zero external network exposure

    #### 🎯 Explore This Digital Twin
    """)

    features = [
        ("🧪 Live Digital Twin", "Adjust process variables with sliders and watch the AI predict optimal setpoints in real-time."),
        ("📊 Period Comparison", "Compare all 3 periods (FY 23-24 Legacy, FY 24-25 AI Y1, FY 25-26 AI Y2) across 30+ metrics."),
        ("🎓 Model Card & Accuracy", "How the model was trained, what drives it, proof of 99.83% prediction accuracy."),
        ("🌱 Impact & Sustainability", "Financial, quality and environmental outcomes — every claim certified."),
    ]
    for icon_label, desc in features:
        st.markdown(f"**{icon_label}** — {desc}")

with col_right:
    st.markdown("### 🏛️ Institutional Backbone")
    st.markdown("""
    <div style='background-color:#F5F7FA; padding:16px; border-radius:10px; border-left:4px solid #1F3864;'>
        <p style='margin:0 0 8px 0;'><b>Developed by</b><br>SAIL Digital Transformation Division (SDTD), Ranchi</p>
        <p style='margin:0 0 8px 0;'><b>Plant</b><br>Bokaro Steel Plant · HDGL / CRM-III</p>
        <p style='margin:0 0 8px 0;'><b>Governance</b><br>Plant-level Digital Transformation Committees · ED (Works) chaired</p>
        <p style='margin:0 0 8px 0;'><b>Compliance</b><br>ISMS 27001:2013 · ISO 45001 · 14001 · 50001</p>
        <p style='margin:0;'><b>Programme</b><br><i>Pravartanam</i> — 163 use cases · ₹1,000 Cr+ annualized impact</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("### 🎖️ Certifications")
    st.markdown("""
    - ✅ **Finance & Accounts Dept, BSL** — ₹3.23 Cr savings certified
    - ✅ **Energy Management (ECS), BSL** — 1,500 t CO₂ reduction certified
    - ✅ **Quality Assurance, BSL** — white band elimination verified
    - ✅ **Ministry of Steel** — Chintan Shivir 2025 Top-4
    """)


# ═══════════════════════════════════════════════════════════════════════════════
# TECHNOLOGY ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("### 🛠️ Technology Architecture")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1F3864 0%, #2E74B5 100%);
                color: white; padding: 18px; border-radius: 10px; height: 200px;'>
        <h4 style='margin:0 0 10px 0;'>🧠 AI Engine</h4>
        <ul style='margin:0; padding-left:18px; font-size:0.9em; line-height:1.6;'>
            <li>Multivariate Polynomial Regression (Degree 2 + Ridge)</li>
            <li>XGBoost Ensemble (400 trees, depth 6)</li>
            <li>135,876 training samples · 99.83% accuracy</li>
            <li>Quarterly retraining · LSTM roadmap active</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #C00000 0%, #E74C3C 100%);
                color: white; padding: 18px; border-radius: 10px; height: 200px;'>
        <h4 style='margin:0 0 10px 0;'>⚙️ Physical Layer</h4>
        <ul style='margin:0; padding-left:18px; font-size:0.9em; line-height:1.6;'>
            <li>80 DFF-4 burners · 3 lateral zones (48+16+16)</li>
            <li>AI-driven width-based zone selection</li>
            <li>λ optimized: 1.4 → 2.0 (near-stoichiometric)</li>
            <li>Lean Firing Mode for thin-gauge (&lt;0.6mm)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_c:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #00B050 0%, #27AE60 100%);
                color: white; padding: 18px; border-radius: 10px; height: 200px;'>
        <h4 style='margin:0 0 10px 0;'>🔄 Data Pipeline</h4>
        <ul style='margin:0; padding-left:18px; font-size:0.9em; line-height:1.6;'>
            <li>5-minute sampling · 15+ variables</li>
            <li>In-house IoT middleware · MQTT protocol</li>
            <li>Python: NumPy, SciPy, Scikit-learn, XGBoost</li>
            <li>Zero CAPEX · Runs on existing infrastructure</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL QUICK-LOOK
# ═══════════════════════════════════════════════════════════════════════════════
if report:
    st.markdown("---")
    st.markdown("### 🎯 Model Performance Snapshot")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        acc = report.get('cv_accuracy_mean', 0)
        st.metric("CV Accuracy", f"{acc:.2f}%",
                  delta=f"±{report.get('cv_accuracy_std', 0):.2f}%", delta_color="off")
    with c2:
        st.metric("R² Score (5-fold CV)", f"{report.get('cv_r2_mean', 0):.4f}",
                  delta="Held-out validation", delta_color="off")
    with c3:
        st.metric("Mean Absolute Error", f"{report.get('cv_mae_mean', 0):.2f} °C",
                  delta="Zone setpoint prediction", delta_color="off")
    with c4:
        st.metric("Training Samples", f"{report.get('training_samples', 0):,}",
                  delta=f"{report.get('n_features', 0)} features · {report.get('n_targets', 0)} targets",
                  delta_color="off")


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#595959; font-size:0.85em; padding:12px;'>
    <b>SAIL Digital Twin v1.1</b> · Built with ❤️ by SAIL Digital Transformation Division, Ranchi<br>
    <i>Made in India · Atmanirbhar Bharat in industrial AI</i>
</div>
""", unsafe_allow_html=True)
