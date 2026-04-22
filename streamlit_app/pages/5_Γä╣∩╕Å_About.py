"""
═══════════════════════════════════════════════════════════════════════════════
 SAIL Digital Twin — Page 5: About
═══════════════════════════════════════════════════════════════════════════════
 Project credits, team, technology stack, and how to navigate the dashboard.
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.styling import (
    apply_custom_theme, render_header,
    render_section_divider, SAIL_NAVY, SAIL_RED, SAIL_GREEN,
)


st.set_page_config(page_title="About | SAIL Digital Twin", page_icon="ℹ️", layout="wide")
apply_custom_theme()

render_header(
    title="ℹ️ About This Digital Twin",
    subtitle="Project credits, technical stack, and how to use this dashboard",
    context="Built for the ICC Technology Excellence Awards 2026 — Emerging Technology Adoption (Large)"
)


# ═══════════════════════════════════════════════════════════════════════════════
# PROJECT BACKGROUND
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("### 🎯 What This Digital Twin Represents")

st.markdown("""
This interactive dashboard is a **working replica** of the AI-Assisted Intelligent Stoichiometric
Optimization system currently running on SAIL Bokaro's Hot Dip Galvanizing Line (HDGL / CRM-III).

The actual production AI executes **every 5 minutes, 24 × 7**, sampling live plant signals and
writing optimal zone setpoints back to the furnace controllers. This dashboard lets viewers
**see, interact with, and validate** the same inference engine that generated
₹3.23 crores in year-1 savings and 1,500 tonnes of avoided CO₂.

For the ICC Grand Jury, this tool exists so **no claim needs to be taken on faith** — every
number is traceable to data, every prediction to a mathematical equation, every impact to a
certified department signature.
""")


render_section_divider()


# ═══════════════════════════════════════════════════════════════════════════════
# HOW TO USE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("### 🧭 How to Navigate")

c1, c2 = st.columns(2)
with c1:
    st.markdown("""
    #### 🧪 **Live Digital Twin**
    Adjust process variables with sliders — thickness, width, line speed, pot temperature,
    induction power, DFF exit temperature — and see the AI predict optimal zone setpoints
    in real time. Presets let you jump to common operating scenarios.

    #### 📊 **Period Comparison**
    Year-over-year comparison between FY 23-24 (Legacy baseline) and FY 24-25 (AI deployed):
    daily production trends, power efficiency, product mix, setpoint tracking quality.
    """)

with c2:
    st.markdown("""
    #### 🎓 **Model Card**
    How the AI was built — architecture, training data, feature importance,
    validation metrics with >98% cross-validated accuracy, and the explicit equation
    (no black box).

    #### 🌱 **Impact & Sustainability**
    Financial, quality, and environmental outcomes with fully transparent calculations.
    Every claim traceable to a certified department signature.
    """)


render_section_divider()


# ═══════════════════════════════════════════════════════════════════════════════
# TECHNOLOGY STACK
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("### 🛠️ Technology Stack (100% Open Source)")

cc1, cc2, cc3 = st.columns(3)

with cc1:
    st.markdown("""
    #### Data & ML Core
    - **Python 3.10+** — Language
    - **pandas** — Data manipulation
    - **NumPy / SciPy** — Numerical foundation
    - **scikit-learn** — Polynomial regression, Ridge, pipelines
    - **XGBoost** — Gradient boosting ensemble
    - **joblib** — Model persistence
    """)

with cc2:
    st.markdown("""
    #### Visualization & UI
    - **Streamlit** — Dashboard framework
    - **Plotly** — Interactive charts
    - **Matplotlib / Seaborn** — Notebook charts
    - **Custom CSS** — SAIL brand theming
    """)

with cc3:
    st.markdown("""
    #### Production Integration
    - **MQTT** — PLC ↔ AI middleware
    - **OPC-UA** — Plant automation protocol
    - **Siemens PCS 7** — Existing DCS (unchanged)
    - **In-house IoT layer** — Custom data bridge
    """)


render_section_divider()


# ═══════════════════════════════════════════════════════════════════════════════
# PROJECT TEAM
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("### 👥 Project Team")

st.markdown("""
This project is a collaboration between **SAIL Digital Transformation Division (SDTD)** at
Ranchi and **SAIL Bokaro Steel Plant's** process, automation, and quality teams.

- **Programme:** _Pravartanam_ — SAIL's enterprise-wide digital transformation
- **Project Lead (Digital):** SDTD, Ranchi
- **Plant Counterparts:** HDGL / CRM-III operations, automation, F&A, ECS, QA teams — Bokaro Steel Plant
- **Governance:** Plant-level Digital Transformation Committee, chaired by the Executive Director (Works)
- **Patent Application:** Filed under Indian Patent Office (sister project ACCURATE 5.0 — App. No. 202331024697)
""")


render_section_divider()


# ═══════════════════════════════════════════════════════════════════════════════
# ACKNOWLEDGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("### 🙏 Acknowledgement")

st.markdown("""
Special thanks to:

- **Ministry of Steel, Government of India** — for featuring this project at Chintan Shivir November 2025
- **Executive Director (Works) & SAIL Bokaro Leadership** — for sponsoring the governance framework
- **HDGL operations, automation, and maintenance teams** — for trusting the AI enough to let it run
- **RCL/MTL Testing Lab** — for the metallurgical characterization that traced the root cause
- **All 50,000+ SAIL employees** who, in countless small ways, make the steel that builds modern India

> *"There's a little bit of SAIL in everybody's life — सुई से चंद्रयान तक"*
""")


render_section_divider()


# ═══════════════════════════════════════════════════════════════════════════════
# CONTACT
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("### 📬 Contact & Credits")

st.markdown("""
**Dashboard Version:** 1.0.0
**Last Trained:** See Model Card page
**Code Repository:** Internal SAIL Digital Transformation Division

For queries about this submission, please contact:
**SAIL Digital Transformation Division (SDTD)** · Ranchi, Jharkhand
""")

st.info("""
🇮🇳 **Atmanirbhar Bharat. Digital India. Green Steel Mission.**
This project is a living demonstration of what's possible when Indian engineers choose to
**build rather than buy** — saving money, reducing emissions, and restoring customer trust,
all at once.
""")
