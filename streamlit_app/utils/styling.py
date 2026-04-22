"""
═══════════════════════════════════════════════════════════════════════════════
 SAIL Digital Twin — Custom Theming Module
═══════════════════════════════════════════════════════════════════════════════
 Provides a consistent, professional dashboard look across all pages:
   • SAIL brand palette (navy, red, green accents)
   • Typography refinements (system-friendly fonts)
   • Reusable component helpers (KPI cards, section headers, status badges)
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st


# ─────────────────────────────────────────────────────────────────────────────
# BRAND PALETTE
# ─────────────────────────────────────────────────────────────────────────────
SAIL_NAVY       = "#1F3864"   # Primary brand (headers, titles)
SAIL_RED        = "#C00000"   # Financial/alert accents
SAIL_GREEN      = "#00B050"   # Quality/positive accents
SAIL_TEAL       = "#2E7D7D"   # Environmental accent
SAIL_GOLD       = "#D4A10F"   # Recognition accent
BG_LIGHT        = "#F5F7FA"
BG_CARD         = "#FFFFFF"
TEXT_PRIMARY    = "#1A1A1A"
TEXT_SECONDARY  = "#595959"


def apply_custom_theme():
    """Inject CSS to theme the Streamlit app with SAIL brand identity.

    This is called once per page (at the top of each page file). It overrides
    default Streamlit widget styling to deliver a cohesive, professional look.
    """
    st.markdown(f"""
    <style>
        /* ─── Global layout ─────────────────────────────────────────── */
        .main .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }}

        /* ─── Typography ────────────────────────────────────────────── */
        html, body, [class*="css"] {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
        }}
        h1, h2, h3, h4 {{
            color: {SAIL_NAVY};
            font-weight: 600;
            letter-spacing: -0.01em;
        }}

        /* ─── Sidebar styling ───────────────────────────────────────── */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #FFFFFF 0%, #F5F7FA 100%);
            border-right: 1px solid #E1E4E8;
        }}
        [data-testid="stSidebar"] .sidebar-content {{
            padding: 1rem;
        }}

        /* ─── Metric card elevation ─────────────────────────────────── */
        [data-testid="stMetric"] {{
            background-color: {BG_CARD};
            padding: 16px 20px;
            border-radius: 10px;
            border-left: 4px solid {SAIL_NAVY};
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}
        [data-testid="stMetric"]:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        }}
        [data-testid="stMetricValue"] {{
            color: {SAIL_NAVY};
            font-weight: 700;
            font-size: 1.8em;
        }}
        [data-testid="stMetricLabel"] {{
            color: {TEXT_SECONDARY};
            font-size: 0.85em;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        /* ─── Buttons ───────────────────────────────────────────────── */
        .stButton > button {{
            background: linear-gradient(135deg, {SAIL_NAVY} 0%, #2E5C9E 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 22px;
            font-weight: 600;
            transition: all 0.2s ease;
            box-shadow: 0 2px 6px rgba(31, 56, 100, 0.2);
        }}
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(31, 56, 100, 0.3);
        }}

        /* ─── Tabs ──────────────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 4px;
            background-color: transparent;
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px 8px 0 0;
            padding: 10px 20px;
            font-weight: 500;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {SAIL_NAVY} !important;
            color: white !important;
        }}

        /* ─── Sliders ───────────────────────────────────────────────── */
        .stSlider > div > div > div {{
            background-color: {SAIL_NAVY};
        }}

        /* ─── Expanders ─────────────────────────────────────────────── */
        .streamlit-expanderHeader {{
            background-color: {BG_LIGHT};
            border-radius: 6px;
            font-weight: 500;
        }}

        /* ─── Dataframes ────────────────────────────────────────────── */
        .stDataFrame {{
            border-radius: 8px;
            overflow: hidden;
        }}

        /* ─── Alert boxes ───────────────────────────────────────────── */
        .stAlert {{
            border-radius: 8px;
            border: none;
        }}

        /* ─── Hide Streamlit branding ───────────────────────────────── */
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        header {{ visibility: hidden; }}

        /* ─── Custom brand gradient divider ─────────────────────────── */
        .brand-divider {{
            height: 3px;
            background: linear-gradient(90deg, {SAIL_RED} 0%, {SAIL_NAVY} 50%, {SAIL_GREEN} 100%);
            border: none;
            margin: 12px 0 20px 0;
            border-radius: 2px;
        }}
    </style>
    """, unsafe_allow_html=True)


def render_header(title: str, subtitle: str = "", context: str = ""):
    """Render a consistent page header with SAIL brand styling.

    Args:
        title: Main page title (largest)
        subtitle: Explanatory sub-title (smaller)
        context: Small contextual label (site, plant, etc.)
    """
    html = f"""
    <div style='padding: 12px 0 8px 0;'>
        <h1 style='margin:0; color:{SAIL_NAVY}; font-size:2.2em; letter-spacing:-0.02em;'>
            {title}
        </h1>
    """
    if subtitle:
        html += f"""
        <p style='margin:4px 0 0 0; color:{TEXT_SECONDARY}; font-size:1.05em; font-weight:400;'>
            {subtitle}
        </p>
        """
    if context:
        html += f"""
        <p style='margin:2px 0 0 0; color:{TEXT_SECONDARY}; font-size:0.85em; font-style:italic;'>
            {context}
        </p>
        """
    html += "<hr class='brand-divider'/></div>"

    st.markdown(html, unsafe_allow_html=True)


def render_kpi_card(label: str, value: str, delta: str = "",
                    color: str = None, icon: str = ""):
    """Render a visually elevated KPI card.

    Args:
        label: Small label at top
        value: Main headline value (bold)
        delta: Small caption beneath value
        color: Accent color on left border (default: navy)
        icon: Optional emoji or symbol
    """
    color = color or SAIL_NAVY
    html = f"""
    <div style='background: white;
                padding: 20px 22px;
                border-radius: 10px;
                border-left: 5px solid {color};
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                height: 125px;
                display: flex;
                flex-direction: column;
                justify-content: center;'>
        <div style='display:flex; align-items:center; margin-bottom: 6px;'>
            <span style='font-size: 1.2em; margin-right: 8px;'>{icon}</span>
            <span style='color: {TEXT_SECONDARY};
                         font-size: 0.8em;
                         text-transform: uppercase;
                         letter-spacing: 0.05em;
                         font-weight: 600;'>{label}</span>
        </div>
        <div style='color: {color}; font-size: 1.7em; font-weight: 700; line-height: 1.1;'>
            {value}
        </div>
        <div style='color: {TEXT_SECONDARY}; font-size: 0.82em; margin-top: 4px;'>
            {delta}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_status_badge(text: str, status: str = "success"):
    """Render an inline status badge (success/warning/info).

    Args:
        text: Badge text
        status: One of 'success', 'warning', 'info', 'neutral'
    """
    colors = {
        'success': SAIL_GREEN,
        'warning': SAIL_GOLD,
        'info': SAIL_NAVY,
        'neutral': TEXT_SECONDARY,
        'alert': SAIL_RED,
    }
    bg = colors.get(status, SAIL_NAVY)
    html = f"""
    <span style='display:inline-block;
                 background-color: {bg}15;
                 color: {bg};
                 padding: 3px 10px;
                 border-radius: 12px;
                 font-size: 0.78em;
                 font-weight: 600;
                 border: 1px solid {bg}40;'>
        {text}
    </span>
    """
    return html


def render_section_divider(label: str = ""):
    """A subtle section break used between logical groupings on a page."""
    if label:
        st.markdown(f"""
        <div style='margin: 30px 0 10px 0;'>
            <h3 style='color: {SAIL_NAVY}; font-size: 1.15em; margin:0;'>{label}</h3>
            <hr class='brand-divider' style='margin-top: 8px;'/>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<hr class='brand-divider'/>", unsafe_allow_html=True)
