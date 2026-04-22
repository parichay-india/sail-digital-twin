"""
═══════════════════════════════════════════════════════════════════════════════
 SAIL Digital Twin — Data & Model Loader (Google Drive-aware)
═══════════════════════════════════════════════════════════════════════════════
 Paths resolved in priority order:
   1. Environment variable  SAIL_DRIVE_FOLDER
   2. Google Drive mount at /content/drive/MyDrive/SAIL_Digital_Twin
   3. Project-local fallback (sail_digital_twin/models & sail_digital_twin/data)
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os
from pathlib import Path
from typing import Tuple, List


# ─────────────────────────────────────────────────────────────────────────────
# PATH RESOLUTION
# ─────────────────────────────────────────────────────────────────────────────
def resolve_paths():
    """Figure out where models and data live — Drive preferred, local fallback."""
    # Priority 1 — explicit env variable
    env_folder = os.environ.get('SAIL_DRIVE_FOLDER')
    if env_folder and os.path.isdir(env_folder):
        base = Path(env_folder)
        return base / 'models', base / 'data_processed'

    # Priority 2 — Google Drive mount
    drive_candidates = [
        '/content/drive/MyDrive/SAIL_Digital_Twin',
        os.path.expanduser('~/Google Drive/SAIL_Digital_Twin'),
        os.path.expanduser('~/GoogleDrive/SAIL_Digital_Twin'),
    ]
    for c in drive_candidates:
        if os.path.isdir(c):
            base = Path(c)
            mf = base / 'models'
            df = base / 'data_processed'
            if mf.exists() and (mf / 'scaler.pkl').exists():
                return mf, df

    # Priority 3 — project-local
    here = Path(__file__).parent.parent.parent
    return here / 'models', here / 'data'


MODEL_DIR, DATA_DIR = resolve_paths()

REQUIRED_ARTIFACTS = [
    'scaler.pkl', 'xgb_models.pkl', 'mvpr_models.pkl',
    'feature_metadata.pkl', 'target_metadata.pkl',
    'performance_report.pkl', 'feature_cols.pkl', 'target_cols.pkl',
]


# ─────────────────────────────────────────────────────────────────────────────
# UTILITIES
# ─────────────────────────────────────────────────────────────────────────────
def check_artifacts_present() -> Tuple[bool, List[str]]:
    missing = [f for f in REQUIRED_ARTIFACTS if not (MODEL_DIR / f).exists()]
    return len(missing) == 0, missing


def get_path_info() -> dict:
    return {
        'model_dir':    str(MODEL_DIR),
        'data_dir':     str(DATA_DIR),
        'model_dir_ok': MODEL_DIR.exists(),
        'data_dir_ok':  DATA_DIR.exists(),
    }


# ─────────────────────────────────────────────────────────────────────────────
# MODEL ARTIFACT LOADERS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner='Loading feature scaler...')
def load_scaler():
    return joblib.load(MODEL_DIR / 'scaler.pkl')


@st.cache_resource(show_spinner='Loading XGBoost ensemble...')
def load_xgb_models():
    return joblib.load(MODEL_DIR / 'xgb_models.pkl')


@st.cache_resource(show_spinner='Loading MVPR models...')
def load_mvpr_models():
    return joblib.load(MODEL_DIR / 'mvpr_models.pkl')


@st.cache_resource
def load_feature_metadata() -> dict:
    return joblib.load(MODEL_DIR / 'feature_metadata.pkl')


@st.cache_resource
def load_target_metadata() -> dict:
    return joblib.load(MODEL_DIR / 'target_metadata.pkl')


@st.cache_resource
def load_performance_report() -> dict:
    try:
        return joblib.load(MODEL_DIR / 'performance_report.pkl')
    except FileNotFoundError:
        return {}


@st.cache_resource
def load_feature_cols() -> list:
    return joblib.load(MODEL_DIR / 'feature_cols.pkl')


@st.cache_resource
def load_target_cols() -> list:
    return joblib.load(MODEL_DIR / 'target_cols.pkl')


# ─────────────────────────────────────────────────────────────────────────────
# DATASET LOADERS — PER PERIOD
# ─────────────────────────────────────────────────────────────────────────────
def _load_parquet(name: str) -> pd.DataFrame:
    path = DATA_DIR / name
    return pd.read_parquet(path) if path.exists() else pd.DataFrame()


@st.cache_data(show_spinner='Loading hourly Period A (FY 23-24 Legacy)...')
def load_hourly_period_a() -> pd.DataFrame:
    return _load_parquet('hourly_period_A.parquet')


@st.cache_data(show_spinner='Loading hourly Period B1 (FY 24-25 AI Y1)...')
def load_hourly_period_b1() -> pd.DataFrame:
    return _load_parquet('hourly_period_B1.parquet')


@st.cache_data(show_spinner='Loading hourly Period B2 (FY 25-26 AI Y2)...')
def load_hourly_period_b2() -> pd.DataFrame:
    return _load_parquet('hourly_period_B2.parquet')


@st.cache_data
def load_daily_period_a() -> pd.DataFrame:
    return _load_parquet('daily_period_A.parquet')


@st.cache_data
def load_daily_period_b1() -> pd.DataFrame:
    return _load_parquet('daily_period_B1.parquet')


@st.cache_data
def load_daily_period_b2() -> pd.DataFrame:
    return _load_parquet('daily_period_B2.parquet')


@st.cache_data
def load_sample_period_a() -> pd.DataFrame:
    return _load_parquet('sample_period_A.parquet')


@st.cache_data
def load_sample_period_b1() -> pd.DataFrame:
    return _load_parquet('sample_period_B1.parquet')


@st.cache_data
def load_sample_period_b2() -> pd.DataFrame:
    return _load_parquet('sample_period_B2.parquet')


@st.cache_data
def load_kpi_summary() -> pd.DataFrame:
    """CERTIFIED claims — single source of truth."""
    return _load_parquet('kpi_summary.parquet')


# ─────────────────────────────────────────────────────────────────────────────
# BACKWARD-COMPAT WRAPPERS (B = B1+B2 combined)
# ─────────────────────────────────────────────────────────────────────────────
def load_daily_period_b() -> pd.DataFrame:
    b1, b2 = load_daily_period_b1(), load_daily_period_b2()
    if b1.empty and b2.empty:
        return pd.DataFrame()
    return pd.concat([b1, b2], ignore_index=True).sort_values('Date')


def load_hourly_period_b() -> pd.DataFrame:
    b1, b2 = load_hourly_period_b1(), load_hourly_period_b2()
    if b1.empty and b2.empty:
        return pd.DataFrame()
    return pd.concat([b1, b2], ignore_index=True).sort_values('mydate')


def load_sample_period_b() -> pd.DataFrame:
    b1, b2 = load_sample_period_b1(), load_sample_period_b2()
    if b1.empty and b2.empty:
        return pd.DataFrame()
    return pd.concat([b1, b2], ignore_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# INFERENCE
# ─────────────────────────────────────────────────────────────────────────────
def predict_setpoints(inputs: dict, model_type: str = 'ensemble') -> dict:
    scaler       = load_scaler()
    xgb_models   = load_xgb_models()
    mvpr_models  = load_mvpr_models()
    feature_cols = load_feature_cols()
    target_cols  = load_target_cols()

    X = np.array([[inputs[f] for f in feature_cols]])
    X_scaled = scaler.transform(X)

    preds = {}
    for t in target_cols:
        p_xgb  = float(xgb_models[t].predict(X_scaled)[0])
        p_mvpr = float(mvpr_models[t].predict(X_scaled)[0])
        if model_type == 'xgboost':
            preds[t] = p_xgb
        elif model_type == 'mvpr':
            preds[t] = p_mvpr
        else:
            preds[t] = (p_xgb + p_mvpr) / 2.0
    return preds


def predict_batch(inputs_df: pd.DataFrame, model_type: str = 'ensemble') -> pd.DataFrame:
    scaler       = load_scaler()
    xgb_models   = load_xgb_models()
    mvpr_models  = load_mvpr_models()
    feature_cols = load_feature_cols()
    target_cols  = load_target_cols()

    X = inputs_df[feature_cols].values
    X_scaled = scaler.transform(X)

    out = pd.DataFrame(index=inputs_df.index)
    for t in target_cols:
        p_xgb  = xgb_models[t].predict(X_scaled)
        p_mvpr = mvpr_models[t].predict(X_scaled)
        if model_type == 'xgboost':
            out[t] = p_xgb
        elif model_type == 'mvpr':
            out[t] = p_mvpr
        else:
            out[t] = (p_xgb + p_mvpr) / 2.0
    return out
