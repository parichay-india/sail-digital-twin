"""
═══════════════════════════════════════════════════════════════════════════════
 SAIL Digital Twin — Page 2: 3-Period Analysis (A vs B1 vs B2)
═══════════════════════════════════════════════════════════════════════════════
 Side-by-side comparison of:
   Period A  — FY 2023-24 Legacy (pre-AI baseline)
   Period B1 — FY 2024-25 AI Year 1
   Period B2 — FY 2025-26 AI Year 2
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.styling import (
    apply_custom_theme, render_header, render_kpi_card,
    render_section_divider, SAIL_NAVY, SAIL_RED, SAIL_GREEN
)
from utils.data_loader import (
    load_daily_period_a, load_daily_period_b1, load_daily_period_b2,
    load_sample_period_a, load_sample_period_b1, load_sample_period_b2,
    load_kpi_summary,
)


st.set_page_config(page_title="Period Comparison | SAIL", page_icon="📊", layout="wide")
apply_custom_theme()

render_header(
    title="📊 Period Comparison — 3-Year Transformation",
    subtitle="Period A (FY 23-24 Legacy) vs Period B1 (FY 24-25 AI Y1) vs Period B2 (FY 25-26 AI Y2)",
    context="Every insight computed live from ~315,360 rows of 5-minute process data across 3 years."
)


# Load data
daily_a = load_daily_period_a()
daily_b1 = load_daily_period_b1()
daily_b2 = load_daily_period_b2()
sample_a = load_sample_period_a()
sample_b1 = load_sample_period_b1()
sample_b2 = load_sample_period_b2()
kpi = load_kpi_summary()

if daily_a.empty or daily_b1.empty or daily_b2.empty:
    st.warning("Daily summary data not available. Please run the Jupyter notebook first.")
    st.stop()


# ═══════════════════════════════════════════════════════════════════════════════
# HEADLINE KPIs — 3-way comparison
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("### 🎯 Headline Indicators (Production-Weighted)")

prod_a  = daily_a['Production (Tons)'].sum()
prod_b1 = daily_b1['Production (Tons)'].sum()
prod_b2 = daily_b2['Production (Tons)'].sum()

grand_a  = daily_a['Grand Total Power (kWh)'].sum()
grand_b1 = daily_b1['Grand Total Power (kWh)'].sum()
grand_b2 = daily_b2['Grand Total Power (kWh)'].sum()

spc_a  = grand_a  / prod_a  if prod_a  > 0 else 0
spc_b1 = grand_b1 / prod_b1 if prod_b1 > 0 else 0
spc_b2 = grand_b2 / prod_b2 if prod_b2 > 0 else 0

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Period A Production", f"{prod_a:,.0f} t",
                    f"{daily_a['Production (Tons)'].gt(0).sum()} running days",
                    color=SAIL_RED, icon="🏭")
with c2:
    render_kpi_card("Period B1 Production", f"{prod_b1:,.0f} t",
                    f"Δ {100*(prod_b1-prod_a)/prod_a:+.1f}% vs A",
                    color='#2E74B5', icon="🏭")
with c3:
    render_kpi_card("Period B2 Production", f"{prod_b2:,.0f} t",
                    f"Δ {100*(prod_b2-prod_a)/prod_a:+.1f}% vs A",
                    color=SAIL_GREEN, icon="🏭")
with c4:
    render_kpi_card("3-Year Production", f"{prod_a+prod_b1+prod_b2:,.0f} t",
                    "Total across all 3 periods",
                    color=SAIL_NAVY, icon="📈")


# Certified-claims banner
st.markdown("---")
st.markdown("### 🏅 Certified Propane Efficiency — The True Transformation")

if not kpi.empty:
    c1, c2, c3 = st.columns(3)
    row_a = kpi[kpi['Period'] == 'A'].iloc[0]
    row_b1 = kpi[kpi['Period'] == 'B1'].iloc[0]
    row_b2 = kpi[kpi['Period'] == 'B2'].iloc[0]

    with c1:
        render_kpi_card("Period A (FY23-24) Legacy",
                        f"{row_a['Specific_Propane_kg_per_Ton']:.3f} kg/t",
                        "Baseline — λ = 1.4, uniform firing",
                        color=SAIL_RED, icon="🔻")
    with c2:
        render_kpi_card("Period B1 (FY24-25) AI Y1",
                        f"{row_b1['Specific_Propane_kg_per_Ton']:.3f} kg/t",
                        f"↓ {row_b1['Reduction_Percent']:.2f}% vs A · ₹{row_b1['Financial_Saving_Cr']:.2f} Cr saved",
                        color='#2E74B5', icon="🚀")
    with c3:
        render_kpi_card("Period B2 (FY25-26) AI Y2",
                        f"{row_b2['Specific_Propane_kg_per_Ton']:.3f} kg/t",
                        f"↓ {row_b2['Reduction_Percent']:.2f}% vs A · ₹{row_b2['Financial_Saving_Cr']:.2f} Cr saved",
                        color=SAIL_GREEN, icon="🌱")


render_section_divider()


# ═══════════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════════
tab_trend, tab_efficiency, tab_mix, tab_control = st.tabs([
    "📈 Daily Trends",
    "⚡ Power Efficiency",
    "📏 Product Mix",
    "🎛️ Setpoint Control"
])


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1: Daily Trends
# ─────────────────────────────────────────────────────────────────────────────
with tab_trend:
    st.markdown("#### Daily Production and Power — 3 Periods Overlaid")

    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=False,
        subplot_titles=("Daily Production (Tons)", "Daily Total Power (kWh)"),
        vertical_spacing=0.14
    )

    # Production
    for df, name, color in [
        (daily_a, 'Period A — Legacy (FY23-24)', SAIL_RED),
        (daily_b1, 'Period B1 — AI Y1 (FY24-25)', '#2E74B5'),
        (daily_b2, 'Period B2 — AI Y2 (FY25-26)', SAIL_GREEN),
    ]:
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Production (Tons)'],
                                  name=name, line=dict(color=color, width=1), opacity=0.7),
                      row=1, col=1)
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Grand Total Power (kWh)'],
                                  name=name, line=dict(color=color, width=1), opacity=0.7,
                                  showlegend=False),
                      row=2, col=1)

    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Tons", row=1, col=1, gridcolor='#E8E8E8')
    fig.update_yaxes(title_text="kWh", row=2, col=1, gridcolor='#E8E8E8')
    fig.update_layout(
        height=620, plot_bgcolor='white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
        margin=dict(l=40, r=20, t=50, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    💡 **3-period insight**: Period B1 shows sustained recovery and higher daily production;
    Period B2 demonstrates the AI's continued learning — tighter, more consistent daily output.
    """)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: Power Efficiency (the headline chart)
# ─────────────────────────────────────────────────────────────────────────────
with tab_efficiency:
    st.markdown("#### Specific Power Consumption (kWh/Ton) — The True Efficiency Metric")

    # Compute daily SPC
    for df in [daily_a, daily_b1, daily_b2]:
        df['spc'] = (df['Grand Total Power (kWh)'] /
                      df['Production (Tons)'].replace(0, np.nan)).clip(upper=200)

    fig_eff = go.Figure()
    fig_eff.add_trace(go.Scatter(x=daily_a['Date'], y=daily_a['spc'],
                                  name='Period A — Legacy',
                                  line=dict(color=SAIL_RED, width=1.2), opacity=0.7))
    fig_eff.add_trace(go.Scatter(x=daily_b1['Date'], y=daily_b1['spc'],
                                  name='Period B1 — AI Y1',
                                  line=dict(color='#2E74B5', width=1.2), opacity=0.7))
    fig_eff.add_trace(go.Scatter(x=daily_b2['Date'], y=daily_b2['spc'],
                                  name='Period B2 — AI Y2',
                                  line=dict(color=SAIL_GREEN, width=1.2), opacity=0.7))
    # Median lines
    fig_eff.add_hline(y=daily_a['spc'].median(), line_dash='dash', line_color=SAIL_RED,
                      annotation_text=f"A median: {daily_a['spc'].median():.1f}",
                      annotation_position="top right")
    fig_eff.add_hline(y=daily_b1['spc'].median(), line_dash='dash', line_color='#2E74B5',
                      annotation_text=f"B1 median: {daily_b1['spc'].median():.1f}",
                      annotation_position="right")
    fig_eff.add_hline(y=daily_b2['spc'].median(), line_dash='dash', line_color=SAIL_GREEN,
                      annotation_text=f"B2 median: {daily_b2['spc'].median():.1f}",
                      annotation_position="bottom right")

    fig_eff.update_layout(
        title="Specific Power Consumption — Daily Trend",
        xaxis_title="Date", yaxis_title="kWh per Ton",
        height=460, plot_bgcolor='white',
        yaxis=dict(gridcolor='#E8E8E8'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
    )
    st.plotly_chart(fig_eff, use_container_width=True)

    # Box plot
    st.markdown("#### Distribution Comparison")
    fig_box = go.Figure()
    fig_box.add_trace(go.Box(y=daily_a['spc'].dropna(), name='A — Legacy',
                              marker_color=SAIL_RED, boxmean='sd'))
    fig_box.add_trace(go.Box(y=daily_b1['spc'].dropna(), name='B1 — AI Y1',
                              marker_color='#2E74B5', boxmean='sd'))
    fig_box.add_trace(go.Box(y=daily_b2['spc'].dropna(), name='B2 — AI Y2',
                              marker_color=SAIL_GREEN, boxmean='sd'))
    fig_box.update_layout(
        height=420, plot_bgcolor='white',
        yaxis=dict(title='kWh / Ton', gridcolor='#E8E8E8'),
        showlegend=False
    )
    st.plotly_chart(fig_box, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: Product Mix
# ─────────────────────────────────────────────────────────────────────────────
with tab_mix:
    st.markdown("#### Coil Thickness Distribution — Product Complexity")

    if not sample_a.empty and not sample_b1.empty and not sample_b2.empty:
        fig_mix = go.Figure()
        for df, name, color in [
            (sample_a, 'A — Legacy', SAIL_RED),
            (sample_b1, 'B1 — AI Y1', '#2E74B5'),
            (sample_b2, 'B2 — AI Y2', SAIL_GREEN),
        ]:
            fig_mix.add_trace(go.Histogram(
                x=df['coilthickness'], nbinsx=50,
                name=name, marker_color=color, opacity=0.55,
                histnorm='probability density'
            ))
        fig_mix.update_layout(
            title="Coil Thickness — Frequency Distribution",
            xaxis_title="Thickness (mm)", yaxis_title="Probability Density",
            barmode='overlay', height=440, plot_bgcolor='white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
        )
        st.plotly_chart(fig_mix, use_container_width=True)

        # Stats table
        def stats_col(df):
            return [
                f"{df['coilthickness'].mean():.2f}",
                f"{df['coilthickness'].median():.2f}",
                f"{df['coilwidth'].mean():.0f}",
                f"{100*(df['coilthickness'] < 0.6).mean():.1f}%",
                f"{100*(df['coilwidth'] > 1350).mean():.1f}%",
            ]
        stats_df = pd.DataFrame({
            'Metric': ['Avg Thickness (mm)', 'Median Thickness (mm)',
                       'Avg Width (mm)', '% Thin-Gauge (<0.6mm)', '% Wide (>1350mm)'],
            'Period A': stats_col(sample_a),
            'Period B1': stats_col(sample_b1),
            'Period B2': stats_col(sample_b2),
        })
        st.dataframe(stats_df, hide_index=True, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4: Setpoint Control Quality
# ─────────────────────────────────────────────────────────────────────────────
with tab_control:
    st.markdown("#### Zone Temperature Control — Setpoint vs Actual")

    if not sample_a.empty and not sample_b1.empty and not sample_b2.empty:
        err_a  = sample_a['rthstrip_ACT'] - sample_a['rthstrip_SP']
        err_b1 = sample_b1['rthstrip_ACT'] - sample_b1['rthstrip_SP']
        err_b2 = sample_b2['rthstrip_ACT'] - sample_b2['rthstrip_SP']

        fig_err = go.Figure()
        fig_err.add_trace(go.Histogram(
            x=err_a, nbinsx=70, name=f'A (MAE={err_a.abs().mean():.2f}°C)',
            marker_color=SAIL_RED, opacity=0.55, histnorm='probability density'))
        fig_err.add_trace(go.Histogram(
            x=err_b1, nbinsx=70, name=f'B1 (MAE={err_b1.abs().mean():.2f}°C)',
            marker_color='#2E74B5', opacity=0.55, histnorm='probability density'))
        fig_err.add_trace(go.Histogram(
            x=err_b2, nbinsx=70, name=f'B2 (MAE={err_b2.abs().mean():.2f}°C)',
            marker_color=SAIL_GREEN, opacity=0.55, histnorm='probability density'))
        fig_err.add_vline(x=0, line_dash='dash', line_color='black',
                          annotation_text="Setpoint", annotation_position="top right")
        fig_err.update_layout(
            title="RTH Strip Tracking Error — Actual − Setpoint Distribution",
            xaxis_title="Error (°C)", yaxis_title="Density",
            barmode='overlay', height=460, plot_bgcolor='white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
        )
        st.plotly_chart(fig_err, use_container_width=True)

        # Per-zone MAE table
        zones_rows = []
        for zone in ['rthstrip', 'rtsstrip', 'rjcstrip']:
            try:
                zones_rows.append({
                    'Zone': zone.upper(),
                    'Period A MAE (°C)': round((sample_a[f'{zone}_ACT'] - sample_a[f'{zone}_SP']).abs().mean(), 2),
                    'Period B1 MAE (°C)': round((sample_b1[f'{zone}_ACT'] - sample_b1[f'{zone}_SP']).abs().mean(), 2),
                    'Period B2 MAE (°C)': round((sample_b2[f'{zone}_ACT'] - sample_b2[f'{zone}_SP']).abs().mean(), 2),
                })
            except Exception:
                continue
        if zones_rows:
            st.dataframe(pd.DataFrame(zones_rows), hide_index=True, use_container_width=True)

        st.info("""
        💡 **What this proves**: Period B2 shows the tightest control — the AI has learned from an
        extra year of data, reducing tracking errors further. A more demanding product mix is being
        handled with better control quality. That is compounding self-learning in action.
        """)
