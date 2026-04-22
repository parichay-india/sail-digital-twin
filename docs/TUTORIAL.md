# 📖 SAIL Digital Twin — Step-by-Step Execution Tutorial

> **Audience:** Anyone running this Digital Twin for the first time — Jury members, SAIL colleagues, auditors, or future developers.
>
> **Time to first dashboard view:** ~15 minutes (first run) · ~3 minutes (subsequent runs — models cached in Drive)
>
> **Environment:** Google Colab (recommended) + Google Drive, or local Python 3.10+

---

## 🧭 Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Google Drive Setup](#2-google-drive-setup)
3. [Running in Google Colab](#3-running-in-google-colab)
4. [Running Locally](#4-running-locally)
5. [Understanding the Notebook](#5-understanding-the-notebook)
6. [Exploring the Dashboard](#6-exploring-the-dashboard)
7. [Smart-Caching Workflow](#7-smart-caching-workflow)
8. [Troubleshooting](#8-troubleshooting)
9. [FAQ](#9-frequently-asked-questions)

---

## 1. Prerequisites

**Required files (provided separately):**
1. `sail_digital_twin/` — the project folder (this codebase)
2. `canonical_dataset/` — contains:
   - `SAIL_Master_Dataset.xlsx` (single-file all-in-one, 2.6 MB)
   - `sail_master_5min.csv` (fast-loading, 74 MB)
   - `sail_daily_summary.csv`
   - `sail_kpi_summary.csv` — the certified claims source of truth

**Required accounts:**
- Google account with enough Drive space (~100 MB for all files)
- Google Colab access (free tier works)

---

## 2. Google Drive Setup

### Step 2.1 — Create the Drive folder structure

In your Google Drive (`MyDrive` root), create this folder tree:

```
MyDrive/
└── SAIL_Digital_Twin/
    ├── dataset/
    ├── models/
    └── data_processed/
```

The `models/` and `data_processed/` folders will be auto-populated by the notebook on first run. You only need to put files in `dataset/`.

### Step 2.2 — Upload the canonical dataset

Upload these files to `MyDrive/SAIL_Digital_Twin/dataset/`:

**Minimum required (for CSV-based workflow, recommended — fastest):**
- `sail_master_5min.csv`
- `sail_daily_summary.csv`
- `sail_kpi_summary.csv`

**Alternative (all-in-one Excel, a bit slower to load):**
- `SAIL_Master_Dataset.xlsx` (contains all sheets in one file)

Both approaches work; pick whichever is more convenient.

---

## 3. Running in Google Colab

### Step 3.1 — Open a new Colab notebook

Go to [colab.research.google.com](https://colab.research.google.com) and create a new notebook (or open the provided `00_COLAB_LAUNCHER.ipynb`).

### Step 3.2 — Upload the project code

Upload `sail_digital_twin.zip` to `/content/` via the Files panel, then in a cell:
```python
import zipfile
with zipfile.ZipFile('/content/sail_digital_twin.zip', 'r') as z:
    z.extractall('/content/')
```

### Step 3.3 — Install dependencies

```python
!pip install -q pandas numpy scipy scikit-learn xgboost joblib \
                matplotlib seaborn plotly openpyxl pyarrow streamlit
```

### Step 3.4 — Train the model (or skip training)

Open `notebooks/01_sail_digital_twin_development.ipynb` and click **Runtime → Run all**.

The notebook will:
1. Mount Google Drive (first-time Google auth prompt appears)
2. Check `MyDrive/SAIL_Digital_Twin/models/` for cached models
3. **If trained models already exist** → skip training, proceed directly to export
4. **If models missing** → load dataset from `MyDrive/SAIL_Digital_Twin/dataset/`, train, save `.pkl` files to `models/`
5. Export per-period Parquet files to `MyDrive/SAIL_Digital_Twin/data_processed/`

Expected final output:
```
🎯 CERTIFIED CLAIMS:
  A (FY 2023-24):  127,490 T · 16.644 kg/T
  B1 (FY 2024-25): 173,201 T · 13.741 kg/T · ₹3.23 Cr · 1,500 t CO₂
  B2 (FY 2025-26): 182,300 T · 12.178 kg/T · ₹5.25 Cr · 2,430 t CO₂

🧠 MODEL: CV Accuracy 99.83% · MAE 1.29°C

🚀 READY FOR STREAMLIT DIGITAL TWIN DEPLOYMENT
```

### Step 3.5 — Launch the dashboard

```python
%cd /content/sail_digital_twin
!streamlit run streamlit_app/app.py --server.headless true &>/content/streamlit_log.txt &
!sleep 5
!npm install -g localtunnel 2>/dev/null
!npx localtunnel --port 8501
```

Click the `https://xxxxx.loca.lt` URL that appears. When the password warning page shows, run in another cell:
```python
!curl https://loca.lt/mytunnelpassword
```

Paste that IP as the password. Your dashboard is now live.

---

## 4. Running Locally

### Step 4.1 — Install Python 3.10+

From [python.org/downloads](https://www.python.org/downloads/).

### Step 4.2 — Install dependencies

```bash
cd sail_digital_twin
pip install -r requirements.txt
```

### Step 4.3 — Option A: Use the pre-bundled models (instant)

Models are already trained and in `sail_digital_twin/models/`. Just launch:

```bash
streamlit run streamlit_app/app.py
```

Open http://localhost:8501.

### Step 4.4 — Option B: Retrain from scratch

Place the canonical dataset in `sail_digital_twin/data/` (or symlink your Drive folder), then:

```bash
jupyter notebook notebooks/01_sail_digital_twin_development.ipynb
# Run all cells
streamlit run streamlit_app/app.py
```

---

## 5. Understanding the Notebook

The notebook has 8 sections, each clearly commented:

| Section | What it does |
|---------|--------------|
| 1 | Dependencies + Google Drive mount |
| 2 | **Smart shortcut:** checks for cached models, sets `SKIP_TRAINING` flag |
| 3 | Loads canonical dataset (CSV preferred, XLSX fallback) |
| 4 | EDA — 3-period transformation chart (A vs B1 vs B2) |
| 5 | Feature engineering (training dataset from B1+B2 running state) |
| 6 | Model training (runs only if `SKIP_TRAINING=False`) — MVPR + XGBoost + 5-fold CV |
| 7 | Saves 8 `.pkl` artifacts + 10 Parquet files to Google Drive |
| 8 | Final readiness summary with certified claims |

---

## 6. Exploring the Dashboard

### 🏠 Home Page
- **Hero KPIs**: ₹8.48 Cr total savings · ~3,930 t CO₂ · 26.83% Y2 efficiency gain
- **Year-by-year cards**: A → B1 → B2 progression
- **Institutional backbone + certifications**

### 🧪 Live Digital Twin *(the most impactful Jury demo)*
1. Start with **Standard Production** preset
2. Switch to **Thin-Gauge Strip (<0.6mm)** — notice Lean Firing Mode alert
3. Switch to **Wide Heavy Strip (>1350mm)** — watch all 80 burners activate
4. Manually tweak line speed — watch setpoints adjust in real-time
5. Expand the audit trail to show raw input → prediction vector

### 📊 Period Comparison
4 tabs: Daily Trends · Power Efficiency · Product Mix · Setpoint Control
Every chart shows all 3 periods (A/B1/B2) overlaid.

### 🎓 Model Card
- **Architecture diagram**: MVPR + XGBoost ensemble
- **Feature importance**: which inputs drive predictions
- **Validation metrics**: 99.83% cross-validated accuracy
- **The explicit equation**: no black-box claims

### 🌱 Impact & Sustainability
- **Financial**: full transparent calculation of ₹3.23 Cr + ₹5.25 Cr
- **Quality**: 3-layer evidence (physics · product · commerce)
- **Environmental**: IPCC-standard CO₂ math + contextual equivalents
- **National**: Atmanirbhar Bharat · Digital India · Green Steel Mission

---

## 7. Smart-Caching Workflow

The most important convenience feature:

```
FIRST RUN                             SUBSEQUENT RUNS
─────────                             ───────────────
1. Mount Drive                        1. Mount Drive
2. Load dataset from dataset/         2. Load dataset from dataset/
3. Train MVPR (4 models)              3. Detect existing models ← SKIP to step 7
4. Train XGBoost (4 models)
5. 5-fold cross-validation
6. Performance report
7. Save 8 .pkl files to models/       7. Proceed to EDA + export
8. Export Parquet files

⏱️ ~3-5 minutes                       ⏱️ ~30 seconds
```

**Force retrain if needed:**
- Open notebook → Section 2 → change `FORCE_RETRAIN = False` to `True`
- OR delete all files in `MyDrive/SAIL_Digital_Twin/models/`
- OR change hyperparameters in Section 6 (triggers natural retrain)

---

## 8. Troubleshooting

### ❌ Problem: "Model artifacts not found" on Streamlit home page
**Cause:** Notebook hasn't been run yet, OR the Streamlit app can't find Drive.
**Fix:**
1. Run the notebook first (it trains and saves to Drive)
2. If running locally, set env var: `export SAIL_DRIVE_FOLDER=/path/to/your/drive/SAIL_Digital_Twin`

### ❌ Problem: "Dataset not found" in notebook Section 3
**Cause:** Files not in `MyDrive/SAIL_Digital_Twin/dataset/`
**Fix:** Upload `sail_master_5min.csv` + `sail_daily_summary.csv` + `sail_kpi_summary.csv` to that folder.

### ❌ Problem: Google Drive mount fails in Colab
**Fix:** Use **Runtime → Restart and run all**. Authorize Google Drive when prompted.

### ❌ Problem: Streamlit shows 99.83% but we want to re-verify
**Fix:** Set `FORCE_RETRAIN = True` in the notebook's skip-training cell, re-run all cells.

### ❌ Problem: Charts not rendering in Colab/localtunnel
**Fix:** Force browser refresh (Ctrl+Shift+R). If still broken, use ngrok instead of localtunnel.

### ❌ Problem: Port 8501 already in use
**Fix:** `streamlit run streamlit_app/app.py --server.port 8502` then tunnel port 8502.

### ❌ Problem: localtunnel asks for password
**Fix:** `!curl https://loca.lt/mytunnelpassword` — that IP is the password.

---

## 9. Frequently Asked Questions

### Q: Why 3 periods instead of just before/after?
**A:** Period A (FY 23-24) is the pre-AI baseline. Period B1 (FY 24-25) is AI Year 1 — this is where ₹3.23 Cr savings were certified by F&A. Period B2 (FY 25-26) is AI Year 2 — shows **compounding learning**: same AI, more training data, deeper savings (₹5.25 Cr). This 3-period view is the proof that self-learning is real.

### Q: How do I verify the ₹3.23 Cr and ₹5.25 Cr numbers are consistent everywhere?
**A:** Open `canonical_dataset/CLAIM_VERIFICATION_MATRIX.xlsx`. Every claim traces back to a row in `sail_kpi_summary.csv`. The Streamlit Impact page, Period Comparison page, and nomination document all read from these same files — they mathematically cannot diverge.

### Q: Can I skip the notebook entirely?
**A:** Yes — models are pre-bundled. Just `streamlit run streamlit_app/app.py` locally, or upload to Colab and launch directly. The notebook is only needed if you want to (a) retrain on new data, or (b) show the Jury how the model was built.

### Q: Where does the "Accuracy = 99.83%" come from?
**A:** 5-fold cross-validation on the primary target `rthstrip_SP`. Accuracy = 100 − MAPE. XGBoost achieves MAPE = 0.17% → Accuracy = 99.83%. You can verify this yourself — run Section 6.5 of the notebook.

### Q: Can I use a totally different dataset?
**A:** Yes, as long as columns match (coilthickness, coilwidth, linespeed, rthstrip_SP, etc.). Update `FEATURE_COLS` and `TARGET_COLS` in Section 5.1 if needed.

### Q: What if my Google Drive folder has a different name?
**A:** Change `DRIVE_FOLDER` in the notebook's Section 1.3, e.g.:
```python
DRIVE_FOLDER = '/content/drive/MyDrive/your_custom_folder_name'
```

---

## 🎯 Next Steps

Once you've explored the dashboard:

- **For Jury members:** Use Live Digital Twin + Impact & Sustainability as primary demo surfaces during Q&A
- **For developers:** Review notebook Section 6 for ML methodology
- **For auditors:** Model Card page has full validation metrics; Impact page has certified numbers; `CLAIM_VERIFICATION_MATRIX.xlsx` cross-references everything

---

## 📞 Support

**SAIL Digital Transformation Division (SDTD)** · Ranchi, Jharkhand

> *Built with ❤️ by SAIL engineers · Made in India · Atmanirbhar Bharat*
