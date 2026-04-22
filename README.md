# 🔥 SAIL Digital Twin — AI-Assisted Stoichiometric Optimization

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sail-digital-twin.streamlit.app)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-SAIL%20Internal-lightgrey)

> **Emerging Technology Adoption — ICC Technology Excellence Awards 2026**
> SAIL Digital Transformation Division · SAIL Bokaro Steel Plant (HDGL / CRM-III)

---

## 📋 What This Is

A **working Digital Twin** of the AI system running on SAIL Bokaro's galvanizing line,
certified to have saved:

- 💰 **₹8.48 Cr** cumulative over 2 years (₹3.23 Cr Y1 + ₹5.25 Cr Y2)
- 🌱 **~3,930 tonnes** of CO₂ avoided cumulative (1,500 t Y1 + 2,430 t Y2)
- ⚡ **26.83%** propane efficiency gain by end of Year 2 (16.644 → 12.178 kg/ton)

The dashboard lets anyone (including the ICC Grand Jury) **interact with the same inference
engine running in production** — moving sliders for coil geometry and line dynamics, watching
the AI predict optimal zone setpoints in real time.

---

## 🌐 Live Dashboard

**Public URL:** https://sail-digital-twin.streamlit.app *(once deployed — see DEPLOYMENT.md)*

---

## 🗓️ Three-Period Timeline (Canonical)

| Period | Fiscal Year | Status | Production | Specific Propane | Savings | CO₂ Avoided |
|:------:|:-----------:|:------:|:----------:|:----------------:|:-------:|:-----------:|
| **A**  | FY 2023-24  | Legacy (pre-AI)  | 127,490 T | 16.644 kg/T | Baseline     | —          |
| **B1** | FY 2024-25  | AI Year 1        | 173,201 T | 13.741 kg/T | ₹3.23 Cr     | 1,500.36 t |
| **B2** | FY 2025-26  | AI Year 2        | 182,300 T | 12.178 kg/T | ₹5.25 Cr     | 2,429.61 t |
| **Cumulative** | | | | | **₹8.48 Cr** | **~3,930 t** |

---

## 🚀 Three Ways to Run

### 1. 🌐 Streamlit Community Cloud (for Jury review)

One-time GitHub-based deployment. Gives a permanent public URL.

→ **See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions** *(~15 minutes)*

### 2. 💻 Local Python (fastest)

Models are pre-bundled. Zero training required:

```bash
pip install -r requirements.txt
streamlit run streamlit_app/app.py
```

Opens at http://localhost:8501

### 3. ☁️ Google Colab (for live development)

For retraining, modifying the model, or demonstrating the notebook workflow to engineers:

```python
# In a Colab cell
!pip install -q pandas numpy scipy scikit-learn xgboost joblib plotly streamlit
# ...then run notebooks/01_sail_digital_twin_development.ipynb
```

→ See [docs/TUTORIAL.md](docs/TUTORIAL.md) for the Colab + Google Drive workflow.

---

## 📂 Project Structure

```
sail-digital-twin/
├── .streamlit/
│   └── config.toml               ← SAIL brand theming for Streamlit
├── .gitignore
├── runtime.txt                    ← Python 3.11 pin for Streamlit Cloud
├── requirements.txt               ← trimmed for cloud deploy
├── README.md                      ← this file
├── DEPLOYMENT.md                  ← step-by-step cloud deployment guide
│
├── streamlit_app/                 ← the dashboard
│   ├── app.py                     ← home page entry point
│   ├── pages/
│   │   ├── 1_🧪_Live_Digital_Twin.py
│   │   ├── 2_📊_Period_Comparison.py
│   │   ├── 3_🎓_Model_Card.py
│   │   ├── 4_🌱_Impact_Sustainability.py
│   │   └── 5_ℹ️_About.py
│   └── utils/
│       ├── styling.py             ← custom theme helpers
│       └── data_loader.py         ← Drive-aware + local fallback
│
├── models/                        ← 8 pre-trained .pkl files (6.6 MB)
├── data/                          ← 10 Parquet files per-period (5 MB)
│
├── notebooks/                     ← Colab / Jupyter notebooks
└── docs/
    └── TUTORIAL.md                ← detailed step-by-step manual
```

---

## 🧠 Model Design

- **Training data:** 135,876 running-state rows from B1 + B2 (AI-deployed) periods
- **Features (10):** coil thickness, width, line speed, pot temperature, VIP-11/12 power, DFF exit temp, POR, entry/exit loops
- **Targets (4):** RTH strip SP, RTS strip SP, RTH zone SP, RTS zone SP
- **Algorithms:** Polynomial Regression (degree 2 + Ridge) + XGBoost (400 trees) ensemble
- **Achieved accuracy:** **99.83% CV** (±0.00% across 5 folds) · MAE 1.29°C · R² 0.83

---

## 🛡️ Production Parallels

| Aspect | This Dashboard | Actual Production System |
|--------|----------------|--------------------------|
| Model | XGBoost + MVPR | Same XGBoost + MVPR |
| Input features | 10 process variables | Same 10 from live PLC |
| Inference cadence | On slider change | Every 5 minutes |
| Network | Public cloud / local | Air-gapped plant network |
| Compliance | N/A (demo) | ISMS 27001:2013 |
| Governance | N/A | DTC chaired by ED (Works) |

---

## 🏆 Recognition

- ✅ **Ministry of Steel** — Featured in **Chintan Shivir 2025** (Top-4 selected projects)
- ✅ **SAIL Bokaro F&A Department** — ₹3.23 Cr Y1 savings certified in writing
- ✅ **SAIL Bokaro Energy Management (ECS)** — 1,500 t CO₂ reduction certified
- ✅ **SAIL Bokaro Quality Assurance** — white band defect elimination verified

---

## 📜 License & Credits

**Built by:** SAIL Digital Transformation Division (SDTD), Ranchi
**For:** ICC Technology Excellence Awards 2026 — Emerging Technology Adoption (Large)
**Technology:** 100% open source (Python, scikit-learn, XGBoost, Streamlit, Plotly)

> *"सुई से चंद्रयान तक — there's a little bit of SAIL in everybody's life"*
