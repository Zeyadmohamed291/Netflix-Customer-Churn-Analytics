from __future__ import annotations

import base64
from html import escape
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from analysis import (
    QUESTION_CODE,
    QUESTIONS,
    clean_data,
    create_question_figure,
    main_result_text,
    result_table,
    run_question,
)


APP_DIR = Path(__file__).resolve().parent
DATA_PATH = APP_DIR / "netflix_customer_churn.csv"
LOGO_TRANSPARENT_PATH = APP_DIR / "netflix_n_transparent.png"
LOGO_FALLBACK_PATH = APP_DIR / "netflix_logo.png"

# Colors matching the Power BI Netflix Dashboard
NETFLIX_RED = "#E50914"
NETFLIX_CRIMSON = "#990008"
CANVAS_BG = "#07090E"
CARD_BG = "#0D1018"
CARD_BORDER = "#1C2232"
TEXT_WHITE = "#FFFFFF"
TEXT_MUTED = "#94A3B8"

# Multi-tone Netflix palette (Red, Crimson, White, Silver, Slate)
NETFLIX_PALETTE = ["#E50914", "#990008", "#FFFFFF", "#CBD5E1", "#8894A6", "#4B5563"]

# ISO Country mappings for world choropleth coverage
REGION_TO_ISO = {
    "North America": [
        "USA", "CAN", "MEX", "GTM", "CUB", "HTI", "DOM", "HND", "NIC", "CRI", "PAN", "JAM"
    ],
    "South America": [
        "BRA", "ARG", "COL", "PER", "VEN", "CHL", "ECU", "BOL", "PRY", "URY", "GUY", "SUR"
    ],
    "Europe": [
        "GBR", "FRA", "DEU", "ITA", "ESP", "UKR", "POL", "ROU", "NLD", "BEL", "CZE", "GRC",
        "PRT", "SWE", "HUN", "AUT", "CHE", "BGR", "DNK", "FIN", "SVK", "NOR", "IRL", "HRV"
    ],
    "Asia": [
        "CHN", "IND", "IDN", "PAK", "BGD", "JPN", "PHL", "VNM", "TUR", "IRN", "THA", "MMR",
        "KOR", "IRQ", "AFG", "SAU", "UZB", "MYS", "YEM", "NPL", "TWN", "LKA", "KAZ", "SYR",
        "KHM", "JOR", "AZE", "ARE", "TJK", "ISR", "LAO", "SGP"
    ],
    "Africa": [
        "NGA", "ETH", "EGY", "COD", "TZA", "ZAF", "KEN", "UGA", "DZA", "SDN", "MAR", "AGO",
        "GHA", "MOZ", "MDG", "CIV", "CMR", "NER", "MLI", "BFA", "MWI", "ZMB", "TCD", "SOM",
        "SEN", "ZWE", "GIN", "RWA", "BEN", "BDI", "TUN", "SSD", "TGO", "SLE", "LBY", "COG"
    ],
    "Oceania": [
        "AUS", "PNG", "NZL", "FJI", "SLB", "VUT", "NCL", "WSM"
    ],
}


def get_logo_base64() -> str:
    """Return base64 string of the transparent Netflix logo."""
    target_path = LOGO_TRANSPARENT_PATH if LOGO_TRANSPARENT_PATH.exists() else LOGO_FALLBACK_PATH
    if target_path.exists():
        with open(target_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""


LOGO_B64 = get_logo_base64()


st.set_page_config(
    page_title="Netflix Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

    :root {
        --netflix-red: #E50914;
        --netflix-dark: #07090E;
        --card-bg: #0D1018;
        --card-border: #1C2232;
        --text-white: #FFFFFF;
        --text-muted: #94A3B8;
    }

    html, body, [class*="css"] {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* ── Header & Toolbar: Transparent and minimal, hide menu/actions only ── */
    header[data-testid="stHeader"],
    .stApp > header {
        background: transparent !important;
        height: 0px !important;
        overflow: visible !important;
        z-index: 999999 !important;
        border: none !important;
    }
    div[data-testid="stToolbar"] {
        display: flex !important;
        background: transparent !important;
        height: 0px !important;
        overflow: visible !important;
        border: none !important;
    }
    [data-testid="stToolbarActions"],
    [data-testid="stStatusWidget"],
    [data-testid="stMainMenu"],
    div[data-testid="stDecoration"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* ── 1. OPEN SIDEBAR BUTTON (When Sidebar is Closed) ── */
    [data-testid="stExpandSidebarButton"],
    button[data-testid="stExpandSidebarButton"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: fixed !important;
        top: 14px !important;
        left: 14px !important;
        z-index: 1000000 !important;
        background: #0E121E !important;
        background-color: #0E121E !important;
        border: 1px solid rgba(229, 9, 20, 0.5) !important;
        border-radius: 8px !important;
        width: 40px !important;
        height: 40px !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.7), 0 0 12px rgba(229, 9, 20, 0.35) !important;
        cursor: pointer !important;
        transition: all 0.22s ease-in-out !important;
    }
    [data-testid="stExpandSidebarButton"]:hover,
    button[data-testid="stExpandSidebarButton"]:hover {
        background: #E50914 !important;
        background-color: #E50914 !important;
        border-color: #FFFFFF !important;
        box-shadow: 0 4px 20px rgba(229, 9, 20, 0.7) !important;
        transform: scale(1.08) !important;
    }
    [data-testid="stExpandSidebarButton"] svg,
    button[data-testid="stExpandSidebarButton"] svg {
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
        color: #FFFFFF !important;
        width: 22px !important;
        height: 22px !important;
    }

    /* ── 2. CLOSE SIDEBAR BUTTON (When Sidebar is Open) ── */
    [data-testid="stSidebarCollapseButton"],
    button[data-testid="stSidebarCollapseButton"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: absolute !important;
        top: 14px !important;
        right: 14px !important;
        left: auto !important;
        z-index: 1000000 !important;
        background: #0E121E !important;
        background-color: #0E121E !important;
        border: 1px solid rgba(229, 9, 20, 0.5) !important;
        border-radius: 8px !important;
        width: 38px !important;
        height: 38px !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.6), 0 0 10px rgba(229, 9, 20, 0.3) !important;
        cursor: pointer !important;
        transition: all 0.22s ease-in-out !important;
    }
    [data-testid="stSidebarCollapseButton"]:hover,
    button[data-testid="stSidebarCollapseButton"]:hover {
        background: #E50914 !important;
        background-color: #E50914 !important;
        border-color: #FFFFFF !important;
        box-shadow: 0 4px 18px rgba(229, 9, 20, 0.6) !important;
        transform: scale(1.08) !important;
    }
    [data-testid="stSidebarCollapseButton"] svg,
    button[data-testid="stSidebarCollapseButton"] svg {
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
        color: #FFFFFF !important;
        width: 20px !important;
        height: 20px !important;
    }

    .stApp {
        background-color: var(--netflix-dark);
        background-image:
            radial-gradient(ellipse at 10% 10%, rgba(229,9,20,0.05), transparent 40%),
            radial-gradient(ellipse at 90% 90%, rgba(37,99,235,0.03), transparent 50%);
        color: var(--text-white);
    }

    /* Widescreen Grid ── */
    .block-container {
        max-width: 98% !important;
        padding-top: 0.6rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }

    /* ── Ultra-Professional Sidebar ── */
    section[data-testid="stSidebar"] {
        background: #0A0D15 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding: 1.2rem 1rem 2rem 1rem !important;
    }
    section[data-testid="stSidebar"] * {
        color: #F8FAFC;
    }

    /* Unboxed Sidebar Header with Generous Gap */
    .sidebar-unboxed-brand {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 0.4rem 0.3rem 1.1rem 0.3rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1.2rem;
    }
    .sidebar-unboxed-logo {
        height: 46px;
        width: auto;
        object-fit: contain;
        filter: drop-shadow(0 0 14px rgba(229, 9, 20, 0.65));
        margin-right: 4px;
        flex-shrink: 0;
    }
    .sidebar-unboxed-text {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .sidebar-unboxed-title {
        font-family: 'Bebas Neue', 'Impact', sans-serif !important;
        font-size: 2.1rem;
        font-weight: 900;
        color: #E50914 !important;
        letter-spacing: 2.5px;
        line-height: 0.95;
        text-shadow: 0 0 16px rgba(229, 9, 20, 0.5);
    }
    .sidebar-unboxed-subtitle {
        font-size: 0.7rem;
        font-weight: 700;
        color: #94A3B8 !important;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        margin-top: 3px;
    }

    /* Sidebar Filter Group Containers */
    .sidebar-filter-box {
        background: #101420;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 10px;
        padding: 0.85rem 0.95rem;
        margin-bottom: 0.9rem;
    }
    .sidebar-box-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.6rem;
        padding-bottom: 0.35rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .sidebar-box-title {
        color: #FFFFFF !important;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .sidebar-box-tag {
        font-size: 0.62rem;
        padding: 2px 6px;
        border-radius: 4px;
        background: rgba(229, 9, 20, 0.2);
        color: #FCA5A5 !important;
        font-weight: 700;
    }

    /* Dark Input Controls in Sidebar */
    section[data-testid="stSidebar"] label {
        color: #94A3B8 !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.2rem !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
    section[data-testid="stSidebar"] div[data-baseweb="base-input"],
    section[data-testid="stSidebar"] input {
        background-color: #151926 !important;
        border: 1px solid #232A3B !important;
        border-radius: 7px !important;
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div:hover,
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div:focus-within {
        border-color: #E50914 !important;
        box-shadow: 0 0 10px rgba(229, 9, 20, 0.3) !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="tag"] {
        background: #E50914 !important;
        border-radius: 4px !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] {
        background-color: #151926 !important;
        border: 1px solid #232A3B !important;
        border-radius: 7px !important;
        padding: 5px 10px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stSlider"] div[role="slider"] {
        background-color: #E50914 !important;
        border: 2px solid #FFFFFF !important;
    }

    /* Sidebar Telemetry Card */
    .sidebar-telemetry-card {
        background: #0E121C;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 0.8rem 0.95rem;
        margin-top: 0.8rem;
    }
    .telemetry-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.35rem;
        font-size: 0.75rem;
    }
    .telemetry-label { color: #94A3B8 !important; font-weight: 600; }
    .telemetry-value { color: #FFFFFF !important; font-weight: 800; }
    .telemetry-bar-bg {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 3px;
        height: 5px;
        overflow: hidden;
        margin-bottom: 0.4rem;
    }
    .telemetry-bar-fill {
        background: linear-gradient(90deg, #E50914, #FF4D4D);
        height: 100%;
        border-radius: 3px;
    }

    /* ── Main Dashboard Top Brand Header (Centered in the Middle) ── */
    .pbi-brand-container {
        display: flex;
        justify-content: center !important;
        align-items: center;
        gap: 22px;
        width: 100%;
        margin: 0.2rem auto 1.1rem auto;
        padding: 0.4rem 0.5rem;
        text-align: center;
    }
    .pbi-brand-logo {
        height: 52px;
        width: auto;
        object-fit: contain;
        filter: drop-shadow(0 0 16px rgba(229, 9, 20, 0.7));
        margin-right: 4px;
        flex-shrink: 0;
    }
    .pbi-brand-text-col {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .pbi-brand-netflix-text {
        font-family: 'Bebas Neue', 'Impact', sans-serif !important;
        font-size: 2.7rem;
        font-weight: 900;
        color: #E50914 !important;
        letter-spacing: 2.5px;
        line-height: 0.92;
        text-shadow: 0 0 22px rgba(229, 9, 20, 0.5);
    }
    .pbi-brand-title-text {
        color: #FFFFFF !important;
        font-size: 1.25rem;
        font-weight: 800;
        line-height: 1.05;
        letter-spacing: 0.5px;
        margin-top: 2px;
    }

    /* ── Power BI KPI Metric Cards (Uniform Netflix Red Aesthetic) ── */
    .pbi-kpi-card {
        background: #0D1018;
        border: 1px solid var(--card-border);
        border-radius: 8px;
        padding: 0.85rem 1.1rem;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
        transition: border-color 0.2s ease, transform 0.2s ease;
    }
    .pbi-kpi-card:hover {
        border-color: rgba(229, 9, 20, 0.7);
        transform: translateY(-2px);
    }
    .pbi-kpi-label {
        color: #FFFFFF !important;
        font-size: 0.88rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        margin-bottom: 0.2rem;
    }
    .pbi-kpi-value {
        color: #E50914 !important;
        font-size: 2.5rem;
        font-weight: 900;
        line-height: 1;
        font-family: 'Outfit', sans-serif;
    }
    .pbi-kpi-sub {
        color: #64748B !important;
        font-size: 0.72rem;
        font-weight: 500;
        margin-top: 0.25rem;
    }

    /* ── Power BI Visual Card Containers (Luxury Executive Polish) ── */
    .pbi-visual-card {
        background: #0D1018 !important;
        border: 1px solid #1C2232 !important;
        border-radius: 10px !important;
        padding: 0.8rem 0.95rem 0.55rem 0.95rem !important;
        margin-bottom: 0.85rem !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.45) !important;
        transition: all 0.25s ease !important;
    }
    .pbi-visual-card:hover {
        border-color: rgba(255, 255, 255, 0.12) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6) !important;
    }
    .pbi-visual-title {
        color: #F8FAFC !important;
        font-family: 'Outfit', -apple-system, sans-serif !important;
        font-size: 0.96rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        letter-spacing: 0.4px !important;
        margin-bottom: 0.45rem !important;
        padding-bottom: 0.35rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.07) !important;
        text-shadow: none !important;
        text-transform: none !important;
    }

    /* ── Tab Hero Section Header ── */
    .tab-hero-header {
        margin-bottom: 1rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .tab-hero-header h2 {
        color: #FFFFFF !important;
        font-size: 1.35rem;
        font-weight: 800;
        margin: 0 0 0.25rem 0;
        letter-spacing: 0.5px;
    }
    .tab-hero-header p {
        color: #94A3B8 !important;
        font-size: 0.88rem;
    }
    /* ── Netflix Executive Tab Navigation Ribbon (Streamlit 1.62 Native) ── */
    div[data-testid="stTabs"],
    .stTabs {
        background: transparent !important;
        border: none !important;
        margin-top: 0.3rem !important;
        margin-bottom: 1.5rem !important;
        width: 100% !important;
    }

    /* Tab List Ribbon Container: Clean dark glass bar with generous gap */
    div[data-testid="stTabs"] [role="tablist"],
    .stTabs [role="tablist"],
    div[role="tablist"] {
        background: #0D1018 !important;
        border: 1px solid #1C2232 !important;
        border-radius: 12px !important;
        padding: 8px 14px !important;
        gap: 16px !important;
        display: flex !important;
        flex-wrap: wrap !important;
        align-items: center !important;
        width: 100% !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5) !important;
        position: relative !important;
    }

    /* Kill default bottom border line on tablist */
    div[data-testid="stTabs"] [role="tablist"]::after,
    .stTabs [role="tablist"]::after,
    div[role="tablist"]::after {
        display: none !important;
        content: none !important;
        height: 0px !important;
        opacity: 0 !important;
    }

    /* Kill default red underline Selection Indicator */
    .react-aria-SelectionIndicator,
    [data-testid="stTab"] .react-aria-SelectionIndicator,
    div[role="tablist"] .react-aria-SelectionIndicator {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
        width: 0px !important;
        opacity: 0 !important;
        background-color: transparent !important;
    }

    /* ── Individual Tab Buttons: Well-spaced, distinct luxury pills ── */
    [data-testid="stTab"],
    div[role="tab"],
    button[role="tab"] {
        background: #141824 !important;
        background-color: #141824 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 8px !important;
        padding: 10px 22px !important;
        margin: 0 4px !important;
        height: auto !important;
        min-height: 42px !important;
        cursor: pointer !important;
        outline: none !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.22s ease-in-out !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* Tab Text Typography */
    [data-testid="stTab"] *,
    div[role="tab"] *,
    button[role="tab"] * {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        color: #94A3B8 !important;
        letter-spacing: 0.5px !important;
        text-transform: none !important;
        white-space: nowrap !important;
        line-height: 1.2 !important;
        transition: color 0.2s ease !important;
    }

    /* Tab Hover */
    [data-testid="stTab"]:hover,
    div[role="tab"]:hover,
    button[role="tab"]:hover,
    [data-testid="stTab"][data-hovered] {
        background-color: #1E2538 !important;
        border-color: rgba(229, 9, 20, 0.45) !important;
        transform: translateY(-1px) !important;
    }
    [data-testid="stTab"]:hover *,
    div[role="tab"]:hover *,
    button[role="tab"]:hover *,
    [data-testid="stTab"][data-hovered] * {
        color: #FFFFFF !important;
    }

    /* ── ACTIVE TAB: Glowing Netflix Red Button ── */
    [data-testid="stTab"][data-selected],
    [data-testid="stTab"][aria-selected="true"],
    div[role="tab"][aria-selected="true"],
    button[role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #E50914 0%, #B20710 100%) !important;
        background-color: #E50914 !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 16px rgba(229, 9, 20, 0.5) !important;
    }
    [data-testid="stTab"][data-selected] *,
    [data-testid="stTab"][aria-selected="true"] *,
    div[role="tab"][aria-selected="true"] *,
    button[role="tab"][aria-selected="true"] * {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        text-shadow: 0 1px 4px rgba(0, 0, 0, 0.6) !important;
    }

    /* Question context & answer strip */
    .question-context {
        padding: 1rem 1.1rem;
        border: 1px solid var(--card-border);
        border-radius: 8px;
        background: #0D1018;
        margin-bottom: 0.8rem;
    }
    .question-context strong {
        display: block;
        margin-bottom: 0.3rem;
        color: #E50914 !important;
        font-size: 0.75rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    .question-context span {
        color: #CBD5E1 !important;
        font-size: 0.92rem;
        line-height: 1.45;
    }
    .answer-strip {
        margin: 0.8rem 0;
        padding: 0.85rem 1.1rem;
        border: 1px solid rgba(229,9,20,0.3);
        border-left: 4px solid #E50914;
        border-radius: 8px;
        background: rgba(229,9,20,0.08);
        color: #FFFFFF !important;
        font-weight: 700;
        font-size: 1rem;
    }

    .footer-note {
        margin-top: 2rem;
        padding-top: 0.8rem;
        border-top: 1px solid var(--card-border);
        color: #475569;
        font-size: 0.78rem;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load_default_data(path: str) -> pd.DataFrame:
    return clean_data(pd.read_csv(path))


@st.cache_data(show_spinner=False)
def load_uploaded_data(file_bytes: bytes) -> pd.DataFrame:
    return clean_data(pd.read_csv(BytesIO(file_bytes)))


def format_number(val: float | int) -> str:
    """Format numbers cleanly like Power BI (e.g. 19K, 13K, 6,107)."""
    if val >= 1_000_000:
        return f"{val / 1_000_000:.1f}M"
    if val >= 10_000:
        return f"{val / 1_000:.0f}K"
    if val >= 1_000:
        return f"{val / 1_000:.1f}K"
    return f"{int(val):,}"


# ─────────────────────────────────────────────────────────────
# TAB 1: PLOTLY CHARTS (POWER BI REPLICA)
# ─────────────────────────────────────────────────────────────

def create_powerbi_map(data: pd.DataFrame) -> go.Figure:
    """World Choropleth Map with Natural Earth projection and sharp contrast."""
    reg_counts = data["region"].value_counts()
    churn_rates = data.groupby("region")["churned"].mean().mul(100)

    rows = []
    for region, count in reg_counts.items():
        iso_list = REGION_TO_ISO.get(region, [])
        c_rate = churn_rates.get(region, 0.0)
        for iso in iso_list:
            rows.append({
                "iso": iso,
                "region": region,
                "customers": count,
                "churn_rate": f"{c_rate:.1f}%",
            })

    map_df = pd.DataFrame(rows)

    if map_df.empty:
        fig = go.Figure()
        fig.update_layout(
            paper_bgcolor="#0D1018",
            plot_bgcolor="#0D1018",
            annotations=[dict(text="No data for current filters", showarrow=False, font=dict(color="#FFF"))],
        )
        return fig

    fig = px.choropleth(
        map_df,
        locations="iso",
        color="customers",
        hover_name="region",
        hover_data={"customers": ":,", "churn_rate": True, "iso": False},
        color_continuous_scale=[
            (0.0, "#240407"),
            (0.35, "#5C080E"),
            (0.7, "#A80B14"),
            (1.0, "#E50914"),
        ],
    )

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#2A3346",
            coastlinewidth=0.8,
            projection_type="natural earth",
            bgcolor="#0D1018",
            landcolor="#121520",
            lakecolor="#0D1018",
            showland=True,
            showocean=True,
            oceancolor="#080A10",
            showcountries=True,
            countrycolor="#1F2637",
            countrywidth=0.7,
        ),
        paper_bgcolor="#0D1018",
        plot_bgcolor="#0D1018",
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=0, b=0),
        height=315,
        dragmode=False,
    )
    return fig


def create_powerbi_horizontal_bar(data: pd.DataFrame, category_col: str = "device") -> go.Figure:
    """Hardware Device Breakdown Horizontal Bar Chart with crisp typography and clean bars."""
    counts = data[category_col].value_counts().sort_values(ascending=True)
    y_labels = list(counts.index)
    x_values = list(counts.values)

    fig = go.Figure(
        go.Bar(
            x=x_values,
            y=y_labels,
            orientation="h",
            marker=dict(
                color="#E50914",
                line=dict(color="rgba(255,255,255,0.08)", width=0.8),
            ),
            text=[f"{v:,}" for v in x_values],
            textposition="auto",
            textfont=dict(color="#FFFFFF", size=10, family="Outfit"),
            hoverinfo="x+y",
            width=0.6,
        )
    )

    fig.update_layout(
        paper_bgcolor="#0D1018",
        plot_bgcolor="#0D1018",
        margin=dict(l=10, r=15, t=10, b=20),
        height=315,
        xaxis=dict(
            showgrid=True,
            gridcolor="#161B26",
            color="#64748B",
            tickfont=dict(size=9, family="Outfit"),
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=False,
            color="#F1F5F9",
            tickfont=dict(size=11, family="Outfit"),
        ),
    )
    return fig


def create_powerbi_top_genres(data: pd.DataFrame) -> go.Figure:
    """Top 5 Genres Vertical Bar Chart matching Power BI multi-tone style."""
    top5 = data["favorite_genre"].value_counts().head(5)
    bar_colors = ["#E50914", "#8B0000", "#F8FAFC", "#CBD5E1", "#64748B"]
    colors_to_use = bar_colors[: len(top5)]

    fig = go.Figure(
        go.Bar(
            x=top5.index,
            y=top5.values,
            marker=dict(
                color=colors_to_use,
                line=dict(color="rgba(255,255,255,0.05)", width=0.8),
            ),
            text=[f"{v:,}" for v in top5.values],
            textposition="outside",
            textfont=dict(color="#F8FAFC", size=10, family="Outfit"),
            hoverinfo="x+y",
            width=0.55,
        )
    )

    fig.update_layout(
        paper_bgcolor="#0D1018",
        plot_bgcolor="#0D1018",
        margin=dict(l=10, r=10, t=25, b=20),
        height=245,
        xaxis=dict(
            showgrid=False,
            color="#CBD5E1",
            tickfont=dict(size=10, family="Outfit"),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#161B26",
            color="#64748B",
            tickfont=dict(size=9),
            zeroline=False,
        ),
    )
    return fig


def create_powerbi_donut(data: pd.DataFrame) -> go.Figure:
    """Content Type Donut Chart with thin ring and clear center total."""
    active_count = int((data["churned"] == 0).sum())
    churned_count = int((data["churned"] == 1).sum())
    total = active_count + churned_count

    labels = ["Active", "Churned"]
    values = [active_count, churned_count]

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.68,
            marker=dict(
                colors=["#E50914", "#F8FAFC"],
                line=dict(color="#0D1018", width=3),
            ),
            textinfo="percent",
            textposition="outside",
            textfont=dict(color="#F8FAFC", size=10, family="Outfit"),
            hoverinfo="label+value+percent",
            showlegend=True,
        )
    )

    fig.update_layout(
        paper_bgcolor="#0D1018",
        plot_bgcolor="#0D1018",
        margin=dict(l=10, r=10, t=10, b=10),
        height=245,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.16,
            xanchor="center",
            x=0.5,
            font=dict(color="#94A3B8", size=10, family="Outfit"),
        ),
        annotations=[
            dict(
                text=f"<b>{format_number(total)}</b><br><span style='font-size:9px;color:#94A3B8;letter-spacing:1px;'>TOTAL</span>",
                x=0.5,
                y=0.5,
                font=dict(size=14, color="#FFFFFF", family="Outfit"),
                showarrow=False,
            )
        ],
    )
    return fig


def create_powerbi_trend(data: pd.DataFrame) -> go.Figure:
    """Smooth Glowing Red Trend Area Chart for Churn Rate by Inactivity Cohorts."""
    bins = [0, 10, 20, 30, 40, 50, 60]
    labels = ["0-10d", "11-20d", "21-30d", "31-40d", "41-50d", "51-60d"]
    binned = pd.cut(data["last_login_days"], bins=bins, labels=labels)
    churn_by_inactivity = data.groupby(binned, observed=False)["churned"].mean().mul(100).fillna(0)

    fig = go.Figure(
        go.Scatter(
            x=labels,
            y=churn_by_inactivity.values,
            mode="lines+markers",
            line=dict(color="#E50914", width=2.8, shape="spline"),
            marker=dict(size=6, color="#E50914", line=dict(color="#FFFFFF", width=1.5)),
            fill="tozeroy",
            fillcolor="rgba(229, 9, 20, 0.14)",
            hoverinfo="x+y",
            hovertemplate="Inactivity: %{x}<br>Churn Rate: %{y:.1f}%<extra></extra>",
            name="Churn Rate (%)",
        )
    )

    fig.update_layout(
        paper_bgcolor="#0D1018",
        plot_bgcolor="#0D1018",
        margin=dict(l=15, r=15, t=20, b=20),
        height=245,
        xaxis=dict(
            showgrid=True,
            gridcolor="#161B26",
            color="#64748B",
            tickfont=dict(size=9, family="Outfit"),
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#161B26",
            color="#64748B",
            tickfont=dict(size=9, family="Outfit"),
            ticksuffix="%",
            zeroline=False,
        ),
    )
    return fig


# ─────────────────────────────────────────────────────────────
# TAB 2 & 3 REFINED CHARTS (NETFLIX RED SYSTEM WITH GRADIENT & AIR)
# ─────────────────────────────────────────────────────────────

def create_refined_horizontal_bar(
    series: pd.Series,
    is_percentage: bool = False,
    height: int = 280,
    gradient_red: bool = True,
) -> go.Figure:
    """Refined horizontal bar chart in Netflix Red with smooth shading and breathable spacing."""
    sorted_s = series.sort_values(ascending=True)

    n = len(sorted_s)
    if gradient_red and n > 1:
        # Subtle crimson-to-vibrant red gradient
        shades = ["#660007", "#8A000A", "#AD000D", "#CC0010", "#E50914", "#FF2A35"]
        colors = shades[-n:]
    else:
        colors = ["#E50914"] * n

    fmt = ".1f" if is_percentage else ","
    suffix = "%" if is_percentage else ""
    labels = [f"{v:{fmt}}{suffix}" for v in sorted_s.values]

    fig = go.Figure(
        go.Bar(
            x=sorted_s.values,
            y=sorted_s.index,
            orientation="h",
            marker=dict(
                color=colors,
                line=dict(color="rgba(255,255,255,0.1)", width=0.8),
            ),
            text=labels,
            textposition="auto",
            textfont=dict(color="#FFFFFF", size=10, family="Outfit"),
            width=0.62,
        )
    )

    fig.update_layout(
        paper_bgcolor="#0D1018",
        plot_bgcolor="#0D1018",
        margin=dict(l=10, r=15, t=10, b=20),
        height=height,
        xaxis=dict(
            showgrid=True,
            gridcolor="#181D2A",
            color="#94A3B8",
            tickfont=dict(size=9),
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=False,
            color="#FFFFFF",
            tickfont=dict(size=10, family="Outfit"),
        ),
    )
    return fig


def create_refined_vertical_bar(
    series: pd.Series,
    is_percentage: bool = False,
    height: int = 280,
    palette_style: str = "netflix_tones",
) -> go.Figure:
    """Refined vertical column chart with Power BI multi-tone Netflix palette."""
    fmt = ".1f" if is_percentage else ","
    suffix = "%" if is_percentage else ""
    labels = [f"{v:{fmt}}{suffix}" for v in series.values]

    if palette_style == "netflix_tones":
        # Exactly matches the Power BI reference image: Red, Crimson, White, Silver, Slate
        colors = (NETFLIX_PALETTE * 2)[: len(series)]
    else:
        colors = ["#E50914"] * len(series)

    fig = go.Figure(
        go.Bar(
            x=series.index,
            y=series.values,
            marker=dict(
                color=colors,
                line=dict(color="rgba(255,255,255,0.08)", width=1),
            ),
            text=labels,
            textposition="outside",
            textfont=dict(color="#FFFFFF", size=10, family="Outfit"),
            width=0.58,
        )
    )

    fig.update_layout(
        paper_bgcolor="#0D1018",
        plot_bgcolor="#0D1018",
        margin=dict(l=10, r=10, t=20, b=20),
        height=height,
        xaxis=dict(
            showgrid=False,
            color="#FFFFFF",
            tickfont=dict(size=10, family="Outfit"),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#181D2A",
            color="#94A3B8",
            tickfont=dict(size=9),
            zeroline=False,
        ),
    )
    return fig


# ─────────────────────────────────────────────────────────────
# DATA LOAD
# ─────────────────────────────────────────────────────────────

try:
    default_base_df = load_default_data(str(DATA_PATH))
except (ValueError, pd.errors.ParserError) as error:
    st.error(f"The dataset could not be loaded: {error}")
    st.stop()


# ─────────────────────────────────────────────────────────────
# ULTRA-PROFESSIONAL SIDEBAR
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    # 1. Unboxed Netflix Brand Header with proper spacing (Gap: 20px)
    logo_elem = (
        f'<img src="data:image/png;base64,{LOGO_B64}" class="sidebar-unboxed-logo" />'
        if LOGO_B64
        else '<span style="font-family:\'Bebas Neue\',sans-serif;font-size:2.2rem;color:#E50914;font-weight:900;">N</span>'
    )
    st.markdown(
        f"""
        <div class="sidebar-unboxed-brand">
            {logo_elem}
            <div class="sidebar-unboxed-text">
                <span class="sidebar-unboxed-title">NETFLIX</span>
                <span class="sidebar-unboxed-subtitle">Analytics Studio</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. Card: Data Source
    st.markdown(
        """
        <div class="sidebar-filter-box">
            <div class="sidebar-box-header">
                <span class="sidebar-box-title">Data Pipeline</span>
                <span class="sidebar-box-tag">Active</span>
            </div>
        """,
        unsafe_allow_html=True,
    )
    data_source_mode = st.radio(
        "Data Source",
        ["Default Dataset", "Upload CSV"],
        horizontal=True,
        label_visibility="collapsed",
    )
    uploaded_file = None
    if data_source_mode == "Upload CSV":
        uploaded_file = st.file_uploader(
            "Upload CSV dataset",
            type=["csv"],
        )
    st.markdown("</div>", unsafe_allow_html=True)


try:
    if uploaded_file is None:
        base_df = default_base_df
        data_source_label = "netflix_customer_churn.csv"
    else:
        base_df = load_uploaded_data(uploaded_file.getvalue())
        data_source_label = uploaded_file.name
except (ValueError, pd.errors.ParserError) as error:
    st.error(f"The dataset could not be loaded: {error}")
    st.stop()


# 3. Card: Slicer Group - Geography & Plan
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-filter-box">
            <div class="sidebar-box-header">
                <span class="sidebar-box-title">Geography & Plan</span>
                <span class="sidebar-box-tag">Filter</span>
            </div>
        """,
        unsafe_allow_html=True,
    )
    selected_subscriptions = st.multiselect(
        "Subscription Type",
        sorted(base_df["subscription_type"].unique()),
        default=[],
        placeholder="All types (Basic, Std, Prem)",
    )

    selected_regions = st.multiselect(
        "Country / Region",
        sorted(base_df["region"].unique()),
        default=[],
        placeholder="All regions",
    )

    age_min = int(base_df["age"].min())
    age_max = int(base_df["age"].max())
    selected_age_range = st.slider(
        "Customer Age Filter",
        min_value=age_min,
        max_value=age_max,
        value=(age_min, age_max),
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # 4. Card: Slicer Group - Audience & Behavior
    st.markdown(
        """
        <div class="sidebar-filter-box">
            <div class="sidebar-box-header">
                <span class="sidebar-box-title">Audience & Behavior</span>
                <span class="sidebar-box-tag">Filter</span>
            </div>
        """,
        unsafe_allow_html=True,
    )
    selected_genres = st.multiselect(
        "Favorite Genre",
        sorted(base_df["favorite_genre"].unique()),
        default=[],
        placeholder="All genres",
    )

    selected_devices = st.multiselect(
        "Device Category",
        sorted(base_df["device"].unique()),
        default=[],
        placeholder="All devices",
    )

    customer_status = st.selectbox(
        "Customer Retention Status",
        ["All customers", "Active customers", "Churned customers"],
    )
    st.markdown("</div>", unsafe_allow_html=True)


# Apply Filters
df = base_df.copy()
if selected_subscriptions:
    df = df[df["subscription_type"].isin(selected_subscriptions)]
if selected_regions:
    df = df[df["region"].isin(selected_regions)]
if selected_genres:
    df = df[df["favorite_genre"].isin(selected_genres)]
if selected_devices:
    df = df[df["device"].isin(selected_devices)]
df = df[(df["age"] >= selected_age_range[0]) & (df["age"] <= selected_age_range[1])]

if customer_status == "Active customers":
    df = df[df["churned"] == 0]
elif customer_status == "Churned customers":
    df = df[df["churned"] == 1]


# 5. Sidebar Telemetry Summary Card
with st.sidebar:
    percent_in_view = (len(df) / len(base_df) * 100) if len(base_df) > 0 else 0
    st.markdown(
        f"""
        <div class="sidebar-telemetry-card">
            <div class="telemetry-row">
                <span class="telemetry-label">Active Records</span>
                <span class="telemetry-value">{len(df):,} / {len(base_df):,}</span>
            </div>
            <div class="telemetry-bar-bg">
                <div class="telemetry-bar-fill" style="width:{percent_in_view:.0f}%;"></div>
            </div>
            <div class="telemetry-row" style="margin-bottom:0;font-size:0.72rem;">
                <span class="telemetry-label">Source</span>
                <span style="color:#CBD5E1;font-weight:600;text-overflow:ellipsis;overflow:hidden;white-space:nowrap;max-width:140px;">{data_source_label}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if df.empty:
    st.warning("No records match the selected slicer filters. Please adjust your filters.")
    st.stop()


# Metrics calculations
total_count = len(df)
active_count = int((df["churned"] == 0).sum())
churned_count = int((df["churned"] == 1).sum())
churn_rate = float(df["churned"].mean() * 100)
avg_watch = float(df["watch_hours"].mean())
total_monthly_fees = float(df["monthly_fee"].sum())


# ─────────────────────────────────────────────────────────────
# MAIN DASHBOARD TABS
# ─────────────────────────────────────────────────────────────

(
    tab_powerbi,
    tab_customers,
    tab_churn,
    tab_questions,
    tab_data,
) = st.tabs(
    [
        "Netflix Power BI Dashboard",
        "Customer Analytics",
        "Churn Intelligence",
        "30 Business Questions",
        "Data Explorer",
    ]
)


# ═════════════════════════════════════════════════════════════
# TAB 1: POWER BI EXACT REPLICA
# ═════════════════════════════════════════════════════════════
with tab_powerbi:
    # ── Centered Main Brand Header (In the Middle) ──
    brand_logo_img = (
        f'<img src="data:image/png;base64,{LOGO_B64}" class="pbi-brand-logo" />'
        if LOGO_B64
        else '<span style="font-family:\'Bebas Neue\',sans-serif;font-size:2.8rem;color:#E50914;font-weight:900;">N</span>'
    )
    st.markdown(
        f"""
        <div class="pbi-brand-container">
            {brand_logo_img}
            <div class="pbi-brand-text-col">
                <div class="pbi-brand-netflix-text">NETFLIX</div>
                <div class="pbi-brand-title-text">Analysis Dashboard</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── 3 Symmetrical Executive KPI Cards Row (Centered & Balanced) ──
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

    with kpi_col1:
        st.markdown(
            f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">Total Subscribers</div>
                <div class="pbi-kpi-value">{format_number(total_count)}</div>
                <div class="pbi-kpi-sub">{total_count:,} total cohort records</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with kpi_col2:
        st.markdown(
            f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">Active Subscribers</div>
                <div class="pbi-kpi-value">{format_number(active_count)}</div>
                <div class="pbi-kpi-sub">{(active_count / total_count * 100):.1f}% active retention</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with kpi_col3:
        st.markdown(
            f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">Churned Subscribers</div>
                <div class="pbi-kpi-value">{format_number(churned_count)}</div>
                <div class="pbi-kpi-sub">{churn_rate:.1f}% attrition rate</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # Middle Row: Global Map (58%) + Horizontal Rating Bar Chart (42%)
    mid_left, mid_right = st.columns([1.38, 1.0])

    with mid_left:
        st.markdown(
            """
            <div class="pbi-visual-card">
                <div class="pbi-visual-title">Global Distribution of Netflix Subscribers</div>
            """,
            unsafe_allow_html=True,
        )
        map_fig = create_powerbi_map(df)
        st.plotly_chart(map_fig, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with mid_right:
        st.markdown(
            """
            <div class="pbi-visual-card">
                <div class="pbi-visual-title">Hardware Device Breakdown</div>
            """,
            unsafe_allow_html=True,
        )
        hbar_fig = create_powerbi_horizontal_bar(df, "device")
        st.plotly_chart(hbar_fig, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Bottom Row: Top 5 Genres (33%) + Content Type Donut (33%) + Trend Area (33%)
    bot_col1, bot_col2, bot_col3 = st.columns([1, 1, 1])

    with bot_col1:
        st.markdown(
            """
            <div class="pbi-visual-card">
                <div class="pbi-visual-title">Top 5 Favorite Genres</div>
            """,
            unsafe_allow_html=True,
        )
        genre_fig = create_powerbi_top_genres(df)
        st.plotly_chart(genre_fig, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with bot_col2:
        st.markdown(
            """
            <div class="pbi-visual-card">
                <div class="pbi-visual-title">Subscriber Retention (Active vs Churned)</div>
            """,
            unsafe_allow_html=True,
        )
        donut_fig = create_powerbi_donut(df)
        st.plotly_chart(donut_fig, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with bot_col3:
        st.markdown(
            """
            <div class="pbi-visual-card">
                <div class="pbi-visual-title">Churn Velocity by Days Inactive</div>
            """,
            unsafe_allow_html=True,
        )
        trend_fig = create_powerbi_trend(df)
        st.plotly_chart(trend_fig, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
# TAB 2: CUSTOMER ANALYTICS (REFINED NETFLIX RED AESTHETIC)
# ═════════════════════════════════════════════════════════════
with tab_customers:
    st.markdown(
        """
        <div class="tab-hero-header">
            <h2>Customer Demographics & Market Distribution</h2>
            <p>Comprehensive audience segmentation across geographic markets, hardware devices, and subscription tiers.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    reg_series = df.groupby("region")["customer_id"].count().sort_values(ascending=False)
    dev_series = df.groupby("device")["customer_id"].count().sort_values(ascending=False)
    genre_series = df.groupby("favorite_genre")["customer_id"].count().sort_values(ascending=False)
    plan_watch = df.groupby("subscription_type")["avg_watch_time_per_day"].mean().loc[["Basic", "Standard", "Premium"]]

    # 4 Executive KPI Cards in Netflix Red
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">Top Market Region</div>
                <div class="pbi-kpi-value" style="font-size:1.8rem;">{reg_series.index[0]}</div>
                <div class="pbi-kpi-sub">{reg_series.iloc[0]:,} customers</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">Primary Hardware</div>
                <div class="pbi-kpi-value" style="font-size:1.8rem;">{dev_series.index[0]}</div>
                <div class="pbi-kpi-sub">{dev_series.iloc[0]:,} active devices</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">Leading Genre</div>
                <div class="pbi-kpi-value" style="font-size:1.8rem;">{genre_series.index[0]}</div>
                <div class="pbi-kpi-sub">{genre_series.iloc[0]:,} audience favorites</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">Avg Daily Watch</div>
                <div class="pbi-kpi-value" style="font-size:1.8rem;">{df['avg_watch_time_per_day'].mean():.2f}h</div>
                <div class="pbi-kpi-sub">Across all accounts</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # Visual Cards Grid (Polished Netflix Palette)
    c_left, c_right = st.columns(2)
    with c_left:
        # Chart 1: Regional Distribution in Shaded Red
        st.markdown(
            """
            <div class="pbi-visual-card">
                <div class="pbi-visual-title">Customer Distribution by Geographic Region</div>
            """,
            unsafe_allow_html=True,
        )
        f_reg = create_refined_horizontal_bar(reg_series, is_percentage=False, height=280, gradient_red=True)
        st.plotly_chart(f_reg, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

        # Chart 3: Plan Watch Time (Red, Crimson, Silver)
        st.markdown(
            """
            <div class="pbi-visual-card">
                <div class="pbi-visual-title">Average Daily Watch Time by Subscription Plan (Hours)</div>
            """,
            unsafe_allow_html=True,
        )
        f_daily = create_refined_vertical_bar(plan_watch, is_percentage=False, height=270, palette_style="netflix_tones")
        st.plotly_chart(f_daily, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c_right:
        # Chart 2: Active Devices Breakdown (Netflix Tones: Red, Crimson, White, Silver, Slate)
        st.markdown(
            """
            <div class="pbi-visual-card">
                <div class="pbi-visual-title">Active Devices Breakdown</div>
            """,
            unsafe_allow_html=True,
        )
        f_dev = create_refined_vertical_bar(dev_series, is_percentage=False, height=280, palette_style="netflix_tones")
        st.plotly_chart(f_dev, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

        # Chart 4: Favorite Genre Preferences (Shaded Red)
        st.markdown(
            """
            <div class="pbi-visual-card">
                <div class="pbi-visual-title">Favorite Genre Preferences</div>
            """,
            unsafe_allow_html=True,
        )
        f_genre = create_refined_horizontal_bar(genre_series, is_percentage=False, height=270, gradient_red=True)
        st.plotly_chart(f_genre, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
# TAB 3: CHURN INTELLIGENCE (REFINED NETFLIX RED AESTHETIC)
# ═════════════════════════════════════════════════════════════
with tab_churn:
    st.markdown(
        """
        <div class="tab-hero-header">
            <h2>Retention & Churn Risk Analytics</h2>
            <p>Diagnostic intelligence analyzing subscriber attrition velocity across subscription tiers, payment gateways, and usage metrics.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sub_churn = df.groupby("subscription_type")["churned"].mean().mul(100).loc[["Basic", "Standard", "Premium"]]
    reg_churn = df.groupby("region")["churned"].mean().mul(100).sort_values(ascending=False)
    dev_churn = df.groupby("device")["churned"].mean().mul(100).sort_values(ascending=False)
    pay_churn = df.groupby("payment_method")["churned"].mean().mul(100).sort_values(ascending=False)

    # 4 Churn KPI Cards in Netflix Red
    ck1, ck2, ck3, ck4 = st.columns(4)
    with ck1:
        st.markdown(
            f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">Overall Churn Rate</div>
                <div class="pbi-kpi-value" style="font-size:2rem;">{churn_rate:.1f}%</div>
                <div class="pbi-kpi-sub">{churned_count:,} churned subscribers</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with ck2:
        st.markdown(
            f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">Highest Risk Tier</div>
                <div class="pbi-kpi-value" style="font-size:1.8rem;">{sub_churn.sort_values(ascending=False).index[0]}</div>
                <div class="pbi-kpi-sub">{sub_churn.max():.1f}% attrition rate</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with ck3:
        st.markdown(
            f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">Highest Risk Region</div>
                <div class="pbi-kpi-value" style="font-size:1.8rem;">{reg_churn.index[0]}</div>
                <div class="pbi-kpi-sub">{reg_churn.iloc[0]:.1f}% attrition rate</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with ck4:
        st.markdown(
            f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">Highest Risk Gateway</div>
                <div class="pbi-kpi-value" style="font-size:1.8rem;">{pay_churn.index[0]}</div>
                <div class="pbi-kpi-sub">{pay_churn.iloc[0]:.1f}% attrition rate</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # Visual Cards Grid in Netflix Palette
    ch_left, ch_right = st.columns(2)
    with ch_left:
        st.markdown(
            """
            <div class="pbi-visual-card">
                <div class="pbi-visual-title">Churn Rate by Subscription Tier (%)</div>
            """,
            unsafe_allow_html=True,
        )
        f1 = create_refined_vertical_bar(sub_churn, is_percentage=True, height=280, palette_style="netflix_tones")
        st.plotly_chart(f1, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="pbi-visual-card">
                <div class="pbi-visual-title">Churn Rate by Hardware Device (%)</div>
            """,
            unsafe_allow_html=True,
        )
        f2 = create_refined_vertical_bar(dev_churn, is_percentage=True, height=270, palette_style="netflix_tones")
        st.plotly_chart(f2, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with ch_right:
        st.markdown(
            """
            <div class="pbi-visual-card">
                <div class="pbi-visual-title">Churn Rate by Geographic Market (%)</div>
            """,
            unsafe_allow_html=True,
        )
        f3 = create_refined_horizontal_bar(reg_churn, is_percentage=True, height=280, gradient_red=True)
        st.plotly_chart(f3, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="pbi-visual-card">
                <div class="pbi-visual-title">Churn Rate by Payment Gateway (%)</div>
            """,
            unsafe_allow_html=True,
        )
        f4 = create_refined_horizontal_bar(pay_churn, is_percentage=True, height=270, gradient_red=True)
        st.plotly_chart(f4, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
# TAB 4: 30 BUSINESS QUESTIONS
# ═════════════════════════════════════════════════════════════
with tab_questions:
    st.markdown(
        """
        <div class="tab-hero-header">
            <h2>30 Business Questions & Analytical Insights</h2>
            <p>Review each strategic business objective, Python analytical code, computed result, and customized visual.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_number = st.selectbox(
        "Select Business Question",
        list(QUESTIONS.keys()),
        format_func=lambda n: f"Question {n:02d}: {QUESTIONS[n]['title_en']}",
    )
    selected_question = QUESTIONS[selected_number]
    selected_result = run_question(df, selected_number)

    st.markdown(f"### Question {selected_number:02d}: {selected_question['title_en']}")

    c_obj, c_val = st.columns(2)
    with c_obj:
        st.markdown(
            f"""
            <div class="question-context">
                <strong>Business Objective</strong>
                <span>{escape(selected_question['objective'])}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c_val:
        st.markdown(
            f"""
            <div class="question-context">
                <strong>Business Value</strong>
                <span>{escape(selected_question['business_value'])}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div class="answer-strip">{escape(main_result_text(selected_result, selected_number))}</div>',
        unsafe_allow_html=True,
    )

    code_col, res_col = st.columns([1.1, 1])
    with code_col:
        st.markdown("#### Analysis Code")
        st.code(QUESTION_CODE[selected_number], language="python", line_numbers=True)
    with res_col:
        st.markdown("#### Calculated Result")
        out_table = result_table(selected_result, selected_number)
        st.dataframe(out_table.round(2), width="stretch", hide_index=True)

    st.markdown("#### Visual Analysis")
    st.markdown(
        """
        <div class="pbi-visual-card" style="padding:1rem;">
        """,
        unsafe_allow_html=True,
    )
    q_fig = create_question_figure(df, selected_number, selected_result)
    st.pyplot(q_fig, width="stretch")
    plt.close(q_fig)
    st.markdown("</div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
# TAB 5: DATA EXPLORER
# ═════════════════════════════════════════════════════════════
with tab_data:
    st.markdown(
        """
        <div class="tab-hero-header">
            <h2>Data Explorer & Segment Export</h2>
            <p>Inspect filtered records, review data quality indicators, and download segment as CSV.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    dm1, dm2, dm3, dm4 = st.columns(4)
    with dm1:
        st.markdown(
            f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">Active Rows</div>
                <div class="pbi-kpi-value" style="font-size:2.2rem;">{df.shape[0]:,}</div>
                <div class="pbi-kpi-sub">Total records in view</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with dm2:
        st.markdown(
            f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">Columns</div>
                <div class="pbi-kpi-value" style="font-size:2.2rem;">{df.shape[1]}</div>
                <div class="pbi-kpi-sub">Dataset dimensions</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with dm3:
        st.markdown(
            f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">Missing Values</div>
                <div class="pbi-kpi-value" style="font-size:2.2rem;">{int(df.isnull().sum().sum()):,}</div>
                <div class="pbi-kpi-sub">100% complete data</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with dm4:
        st.markdown(
            f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">Duplicates</div>
                <div class="pbi-kpi-value" style="font-size:2.2rem;">{int(df.duplicated().sum()):,}</div>
                <div class="pbi-kpi-sub">Clean unique records</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown("#### Filtered Dataset Sample")
    st.dataframe(df.head(100), width="stretch", hide_index=True)

    with st.expander("Descriptive Statistics"):
        st.dataframe(df.describe().round(2), width="stretch")

    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Filtered CSV",
        data=csv_bytes,
        file_name="filtered_netflix_customer_data.csv",
        mime="text/csv",
        width="stretch",
    )


st.markdown(
    '<div class="footer-note">Netflix Analysis Dashboard • Power BI Style Edition • Built with Streamlit, Plotly, Pandas, NumPy</div>',
    unsafe_allow_html=True,
)
