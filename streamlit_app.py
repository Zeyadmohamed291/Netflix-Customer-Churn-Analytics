from __future__ import annotations

from html import escape
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
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

RED = "#E50914"
NAVY = "#0F172A"
BLUE = "#2563EB"
GREEN = "#16A34A"
PURPLE = "#7C3AED"
AMBER = "#D97706"


st.set_page_config(
    page_title="Netflix Customer Churn Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;800&display=swap');

    :root {
        --netflix-red: #E50914;
        --deep-bg: #0B0E14;
        --card-bg: rgba(18, 22, 30, 0.85);
        --card-border: rgba(255, 255, 255, 0.10);
        --text-main: #F8FAFC;
        --text-muted: #94A3B8;
    }

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }

    .stApp {
        background-color: var(--deep-bg);
        background-image:
            radial-gradient(ellipse at 10% 40%, rgba(229,9,20,0.06), transparent 50%),
            radial-gradient(ellipse at 90% 20%, rgba(37,99,235,0.05), transparent 50%);
        color: var(--text-main);
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }

    /* ── Global text ── */
    h1, h2, h3, h4, h5, h6,
    p, label, span,
    .stMarkdown, .stMarkdown p, .stMarkdown div {
        color: var(--text-main) !important;
    }
    .stCaption p, div[data-testid="stCaptionContainer"] p {
        color: var(--text-muted) !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #0B1120 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.08) !important;
    }
    section[data-testid="stSidebar"] * {
        color: var(--text-main) !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stMetric"] {
        min-height: auto;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.10);
        border-top: none;
        box-shadow: none;
    }
    section[data-testid="stSidebar"] div[data-testid="stMetricLabel"] p {
        color: #94A3B8 !important;
    }

    /* ── Sidebar inputs ── */
    section[data-testid="stSidebar"] .stMultiSelect > div > div,
    section[data-testid="stSidebar"] .stSelectbox > div > div,
    section[data-testid="stSidebar"] div[data-testid="stFileUploader"] > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        color: var(--text-main) !important;
    }
    section[data-testid="stSidebar"] .stMultiSelect > div > div:hover,
    section[data-testid="stSidebar"] .stSelectbox > div > div:hover {
        border-color: rgba(229,9,20,0.4) !important;
    }
    section[data-testid="stSidebar"] .stMultiSelect > div > div:focus-within,
    section[data-testid="stSidebar"] .stSelectbox > div > div:focus-within {
        border-color: var(--netflix-red) !important;
        box-shadow: 0 0 0 1px var(--netflix-red) !important;
    }
    /* Selected tag pills */
    section[data-testid="stSidebar"] span[data-baseweb="tag"] {
        background: rgba(229,9,20,0.18) !important;
        border: 1px solid rgba(229,9,20,0.4) !important;
        border-radius: 6px !important;
        color: #FCA5A5 !important;
    }
    section[data-testid="stSidebar"] span[data-baseweb="tag"] span {
        color: #FCA5A5 !important;
    }
    /* Tag close button */
    section[data-testid="stSidebar"] span[data-baseweb="tag"] svg {
        fill: #FCA5A5 !important;
    }
    /* Dropdown menu */
    ul[data-testid="stSelectboxVirtualDropdown"],
    div[data-baseweb="popover"] > div {
        background: #141820 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
    }
    li[role="option"] {
        color: var(--text-main) !important;
    }
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {
        background: rgba(229,9,20,0.12) !important;
    }
    /* File uploader */
    section[data-testid="stSidebar"] div[data-testid="stFileUploader"] > div {
        background: transparent !important;
        border: none !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stFileUploader"] section {
        background: rgba(255,255,255,0.04) !important;
        border: 2px dashed rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stFileUploader"] section:hover {
        border-color: rgba(229,9,20,0.4) !important;
        background: rgba(229,9,20,0.04) !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stFileUploader"] button {
        background: rgba(229,9,20,0.15) !important;
        border: 1px solid rgba(229,9,20,0.3) !important;
        color: #FCA5A5 !important;
        border-radius: 8px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stFileUploader"] button:hover {
        background: rgba(229,9,20,0.25) !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stFileUploader"] small {
        color: var(--text-muted) !important;
    }

    .sidebar-brand {
        display: flex; align-items: center; gap: .85rem;
        margin: .15rem 0 .4rem;
    }
    .brand-mark {
        width: 46px; height: 46px;
        display: grid; place-items: center;
        border-radius: 11px;
        background: linear-gradient(135deg, #E50914, #9B0610);
        color: #fff !important;
        font-size: 1.5rem; font-weight: 900;
        box-shadow: 0 8px 20px rgba(229,9,20,0.35);
    }
    .brand-copy strong { display: block; color: #fff; font-size: 1.05rem; letter-spacing: .04em; }
    .brand-copy span   { color: #94A3B8; font-size: .78rem; }

    .sidebar-label {
        margin: .35rem 0 .65rem;
        color: #94A3B8; font-size: .72rem; font-weight: 800; letter-spacing: .13em;
    }

    /* ── Hero ── */
    .hero {
        position: relative; overflow: hidden;
        padding: 2.5rem 2.6rem;
        margin-bottom: 1.4rem;
        border-radius: 22px;
        color: #fff;
        background: linear-gradient(125deg, #0F172A 0%, #182240 55%, #3B0A12 100%);
        border: 1px solid rgba(255,255,255,0.07);
        box-shadow: 0 20px 50px rgba(0,0,0,0.25);
    }
    .hero::after {
        content: ""; position: absolute;
        width: 340px; height: 340px; right: -80px; top: -160px;
        border-radius: 50%;
        background: rgba(229,9,20,0.22);
        pointer-events: none;
    }
    .hero .eyebrow {
        position: relative; z-index: 1;
        display: inline-block; margin-bottom: .8rem;
        color: #FCA5A5;
        font-size: .78rem; font-weight: 800; letter-spacing: .14em;
    }
    .hero h1 {
        position: relative; z-index: 1;
        margin: 0 0 .6rem; 
        color: #FFFFFF !important;
        font-size: clamp(2.1rem, 3.8vw, 3.4rem);
        font-weight: 800; line-height: 1.1;
    }
    .hero p {
        position: relative; z-index: 1;
        max-width: 800px; margin: .5rem 0 0;
        color: #CBD5E1 !important;
        font-size: 1.02rem; line-height: 1.65;
    }

    /* ── Metric Cards ── */
    div[data-testid="stMetric"] {
        min-height: 120px;
        padding: 1rem 1.1rem;
        border: 1px solid var(--card-border);
        border-top: 4px solid var(--netflix-red);
        border-radius: 16px;
        background: var(--card-bg);
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
        backdrop-filter: blur(12px);
        transition: transform .25s ease, box-shadow .25s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(229,9,20,0.12);
    }
    div[data-testid="stMetricLabel"] p {
        color: var(--text-muted) !important;
        font-size: .88rem !important; font-weight: 600 !important;
    }
    div[data-testid="stMetricValue"] {
        color: var(--text-main) !important;
        font-size: 2rem !important; font-weight: 800 !important;
    }
    div[data-testid="stMetricDelta"] {
        color: var(--text-muted) !important;
    }

    /* ── Section Heading ── */
    .section-heading {
        padding: 1rem 1.1rem;
        margin: .3rem 0 1.2rem;
        border: 1px solid var(--card-border);
        border-left: 5px solid var(--netflix-red);
        border-radius: 14px;
        background: var(--card-bg);
    }
    .section-heading h3 {
        margin: 0 0 .25rem;
        color: var(--text-main) !important;
        font-size: 1.2rem; font-weight: 700;
    }
    .section-heading p {
        margin: 0;
        color: var(--text-muted) !important;
        font-size: .92rem; line-height: 1.5;
    }

    /* ── Insight Cards ── */
    .insight-card {
        min-height: 130px;
        padding: 1.1rem 1.15rem;
        border: 1px solid var(--card-border);
        border-top: 3px solid var(--netflix-red);
        border-radius: 16px;
        background: var(--card-bg);
        box-shadow: 0 6px 18px rgba(0,0,0,0.14);
        backdrop-filter: blur(10px);
        transition: transform .25s ease;
    }
    .insight-card:hover {
        transform: translateY(-3px);
    }
    .insight-label {
        color: var(--text-muted) !important;
        font-size: .75rem; font-weight: 800;
        letter-spacing: .08em; text-transform: uppercase;
    }
    .insight-value {
        margin: .4rem 0 .3rem;
        color: var(--text-main) !important;
        font-size: 1.4rem; font-weight: 800; line-height: 1.2;
    }
    .insight-detail {
        color: var(--text-muted) !important;
        font-size: .85rem; line-height: 1.45;
    }

    /* ── Question Context Cards ── */
    .question-context {
        min-height: 120px;
        padding: 1.1rem 1.15rem;
        border: 1px solid var(--card-border);
        border-radius: 14px;
        background: var(--card-bg);
    }
    .question-context strong {
        display: block; margin-bottom: .4rem;
        color: var(--netflix-red) !important;
        font-size: .78rem; letter-spacing: .07em; text-transform: uppercase;
    }
    .question-context span {
        color: #CBD5E1 !important;
        font-size: .94rem; line-height: 1.55;
    }

    /* ── Answer Strip ── */
    .answer-strip {
        margin: 1rem 0;
        padding: 1rem 1.1rem;
        border: 1px solid rgba(229,9,20,0.25);
        border-left: 5px solid var(--netflix-red);
        border-radius: 12px;
        background: rgba(229,9,20,0.08);
        color: var(--text-main) !important;
        font-weight: 700; font-size: 1.05rem;
    }

    /* ── Tabs ── */
    div[data-testid="stTabs"] button {
        color: var(--text-muted) !important;
        font-weight: 700;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--netflix-red) !important;
    }

    /* ── Data elements ── */
    div[data-testid="stDataFrame"],
    div[data-testid="stCode"] {
        direction: ltr; text-align: left;
    }

    /* ── Footer ── */
    .footer-note {
        margin-top: 2rem; padding-top: 1rem;
        border-top: 1px solid var(--card-border);
        color: #94A3B8; font-size: .8rem; text-align: center;
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


def section_heading(title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="section-heading">
            <h3>{escape(title)}</h3>
            <p>{escape(description)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_card(label: str, value: str, detail: str) -> None:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-label">{escape(label)}</div>
            <div class="insight-value">{escape(value)}</div>
            <div class="insight-detail">{escape(detail)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def bar_figure(
    series: pd.Series,
    title: str,
    ylabel: str,
    color: str,
    horizontal: bool = False,
):
    fig, ax = plt.subplots(figsize=(8.2, 4.35))
    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")

    if horizontal:
        series.sort_values().plot(kind="barh", ax=ax, color=color, width=0.68)
        ax.set_xlabel(ylabel, color="#94A3B8")
        ax.set_ylabel("")
        ax.grid(axis="x", alpha=0.1, color="#94A3B8")
    else:
        series.plot(kind="bar", ax=ax, color=color, width=0.68)
        ax.set_ylabel(ylabel, color="#94A3B8")
        ax.set_xlabel("")
        ax.tick_params(axis="x", rotation=20)
        ax.grid(axis="y", alpha=0.1, color="#94A3B8")

    ax.set_title(title, loc="left", pad=15, color="#F8FAFC", fontsize=13, fontweight="bold")
    ax.tick_params(colors="#94A3B8", labelsize=10)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#334155")
    fig.tight_layout()
    return fig


def donut_figure(active_count: int, churned_count: int):
    fig, ax = plt.subplots(figsize=(7.4, 4.35))
    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")
    ax.pie(
        [active_count, churned_count],
        labels=["Active", "Churned"],
        autopct="%1.1f%%",
        startangle=90,
        colors=[GREEN, RED],
        pctdistance=0.76,
        wedgeprops={"width": 0.42, "edgecolor": "#0B0E14", "linewidth": 2},
        textprops={"color": "#F8FAFC", "fontsize": 11, "fontweight": "bold"},
    )
    ax.set_title(
        "Customer Status Distribution",
        loc="left",
        pad=15,
        color="#F8FAFC",
        fontsize=13,
        fontweight="bold",
    )
    fig.tight_layout()
    return fig


def apply_filters(data: pd.DataFrame) -> pd.DataFrame:
    filtered = data.copy()

    with st.sidebar:
        st.markdown('<div class="sidebar-label">FILTERS</div>', unsafe_allow_html=True)
        st.caption("Leave a field empty to include all values.")

        selected_regions = st.multiselect(
            "Region",
            sorted(data["region"].unique()),
            default=[],
            placeholder="All regions",
        )
        selected_subscriptions = st.multiselect(
            "Subscription Type",
            sorted(data["subscription_type"].unique()),
            default=[],
            placeholder="All subscription types",
        )
        selected_devices = st.multiselect(
            "Device",
            sorted(data["device"].unique()),
            default=[],
            placeholder="All devices",
        )
        selected_genders = st.multiselect(
            "Gender",
            sorted(data["gender"].unique()),
            default=[],
            placeholder="All gender groups",
        )
        selected_genres = st.multiselect(
            "Favorite Genre",
            sorted(data["favorite_genre"].unique()),
            default=[],
            placeholder="All genres",
        )
        customer_status = st.selectbox(
            "Customer Status",
            ["All customers", "Active customers", "Churned customers"],
        )

    if selected_regions:
        filtered = filtered[filtered["region"].isin(selected_regions)]
    if selected_subscriptions:
        filtered = filtered[filtered["subscription_type"].isin(selected_subscriptions)]
    if selected_devices:
        filtered = filtered[filtered["device"].isin(selected_devices)]
    if selected_genders:
        filtered = filtered[filtered["gender"].isin(selected_genders)]
    if selected_genres:
        filtered = filtered[filtered["favorite_genre"].isin(selected_genres)]

    if customer_status == "Active customers":
        filtered = filtered[filtered["churned"] == 0]
    elif customer_status == "Churned customers":
        filtered = filtered[filtered["churned"] == 1]

    return filtered


with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="brand-mark">N</div>
            <div class="brand-copy">
                <strong>NETFLIX ANALYTICS</strong>
                <span>Customer Intelligence Dashboard</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown('<div class="sidebar-label">DATA SOURCE</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload another CSV with the same columns (optional)",
        type=["csv"],
    )


try:
    if uploaded_file is None:
        base_df = load_default_data(str(DATA_PATH))
        data_source_label = "netflix_customer_churn.csv"
    else:
        base_df = load_uploaded_data(uploaded_file.getvalue())
        data_source_label = uploaded_file.name
except (ValueError, pd.errors.ParserError) as error:
    st.error(f"The dataset could not be loaded: {error}")
    st.stop()


df = apply_filters(base_df)

with st.sidebar:
    st.divider()
    st.metric("Customers in Current View", f"{len(df):,}")
    st.caption(f"Source: {data_source_label}")


st.markdown(
    """
    <div class="hero">
        <span class="eyebrow">CUSTOMER INTELLIGENCE • RETENTION • ENGAGEMENT</span>
        <h1>Netflix Customer Churn Analytics</h1>
        <p>
            An interactive decision dashboard built with Pandas, NumPy, Matplotlib, and Streamlit.
            Explore customer behavior, churn patterns, and 30 business questions from one professional workspace.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


if df.empty:
    st.warning("No customers match the current filters. Clear or adjust at least one sidebar filter.")
    st.stop()


customer_count = len(df)
active_count = int((df["churned"] == 0).sum())
churned_count = int((df["churned"] == 1).sum())
churn_rate = float(df["churned"].mean() * 100)
average_watch = float(df["watch_hours"].mean())
total_monthly_fees = float(df["monthly_fee"].sum())

metric_columns = st.columns(5)
metric_columns[0].metric("Total Customers", f"{customer_count:,}", border=True)
metric_columns[1].metric("Active Customers", f"{active_count:,}", border=True)
metric_columns[2].metric("Churn Rate", f"{churn_rate:.1f}%", border=True)
metric_columns[3].metric("Average Watch Hours", f"{average_watch:.2f}", border=True)
metric_columns[4].metric("Total Monthly Fees", f"USD {total_monthly_fees:,.0f}", border=True)


(
    executive_tab,
    customer_tab,
    churn_tab,
    questions_tab,
    data_tab,
) = st.tabs(
    [
        "Executive Overview",
        "Customer Analytics",
        "Churn Analysis",
        "30 Business Questions",
        "Data Explorer",
    ]
)


subscription_count = (
    df.groupby("subscription_type")["customer_id"].count().sort_values(ascending=False)
)
region_count = df.groupby("region")["customer_id"].count().sort_values(ascending=False)
device_count = df.groupby("device")["customer_id"].count().sort_values(ascending=False)
genre_count = df.groupby("favorite_genre")["customer_id"].count().sort_values(ascending=False)

subscription_churn = (
    df.groupby("subscription_type")["churned"].mean().mul(100).sort_values(ascending=False)
)
region_churn = df.groupby("region")["churned"].mean().mul(100).sort_values(ascending=False)
device_churn = df.groupby("device")["churned"].mean().mul(100).sort_values(ascending=False)
payment_churn = (
    df.groupby("payment_method")["churned"].mean().mul(100).sort_values(ascending=False)
)


with executive_tab:
    section_heading(
        "Executive Overview",
        "A focused summary of customer scale, market concentration, value, and retention risk.",
    )

    value_by_subscription = (
        df.groupby("subscription_type")["monthly_fee"].sum().sort_values(ascending=False)
    )
    top_subscription = subscription_count.index[0]
    top_region = region_count.index[0]
    highest_churn_plan = subscription_churn.index[0]
    highest_value_plan = value_by_subscription.index[0]

    insight_columns = st.columns(4)
    with insight_columns[0]:
        insight_card(
            "Largest Plan",
            str(top_subscription),
            f"{subscription_count.iloc[0]:,} customers in the current view.",
        )
    with insight_columns[1]:
        insight_card(
            "Largest Region",
            str(top_region),
            f"{region_count.iloc[0]:,} customers in the current view.",
        )
    with insight_columns[2]:
        insight_card(
            "Highest Churn Risk",
            str(highest_churn_plan),
            f"{subscription_churn.iloc[0]:.1f}% churn rate.",
        )
    with insight_columns[3]:
        insight_card(
            "Highest Monthly Value",
            str(highest_value_plan),
            f"USD {value_by_subscription.iloc[0]:,.0f} in monthly fees.",
        )

    st.write("")
    overview_left, overview_right = st.columns(2)
    with overview_left:
        figure = bar_figure(
            subscription_count,
            "Customer Base by Subscription Type",
            "Number of Customers",
            RED,
        )
        st.pyplot(figure, width="stretch")
        plt.close(figure)
    with overview_right:
        figure = donut_figure(active_count, churned_count)
        st.pyplot(figure, width="stretch")
        plt.close(figure)


with customer_tab:
    section_heading(
        "Customer Analytics",
        "Understand where customers are located, how they access the service, and what they prefer to watch.",
    )

    customer_left, customer_right = st.columns(2)
    with customer_left:
        figure = bar_figure(
            region_count,
            "Customers by Region",
            "Number of Customers",
            BLUE,
            horizontal=True,
        )
        st.pyplot(figure, width="stretch")
        plt.close(figure)

        daily_watch_by_subscription = (
            df.groupby("subscription_type")["avg_watch_time_per_day"]
            .mean()
            .sort_values(ascending=False)
        )
        figure = bar_figure(
            daily_watch_by_subscription,
            "Average Daily Watch Time by Subscription",
            "Average Watch Time per Day",
            PURPLE,
        )
        st.pyplot(figure, width="stretch")
        plt.close(figure)

    with customer_right:
        figure = bar_figure(
            device_count,
            "Customers by Device",
            "Number of Customers",
            GREEN,
        )
        st.pyplot(figure, width="stretch")
        plt.close(figure)

        figure = bar_figure(
            genre_count,
            "Favorite Genre Distribution",
            "Number of Customers",
            AMBER,
        )
        st.pyplot(figure, width="stretch")
        plt.close(figure)


with churn_tab:
    section_heading(
        "Churn Analysis",
        "Compare retention risk across customer segments and examine the relationship between engagement and churn.",
    )

    churn_left, churn_right = st.columns(2)
    with churn_left:
        figure = bar_figure(
            subscription_churn,
            "Churn Rate by Subscription Type",
            "Churn Rate (%)",
            RED,
        )
        st.pyplot(figure, width="stretch")
        plt.close(figure)

        figure = bar_figure(
            device_churn,
            "Churn Rate by Device",
            "Churn Rate (%)",
            PURPLE,
        )
        st.pyplot(figure, width="stretch")
        plt.close(figure)

        watch_by_status = df.groupby("churned")["watch_hours"].mean()
        watch_by_status.index = watch_by_status.index.map({0: "Active", 1: "Churned"})
        figure = bar_figure(
            watch_by_status,
            "Average Watch Hours: Active vs Churned",
            "Average Watch Hours",
            GREEN,
        )
        st.pyplot(figure, width="stretch")
        plt.close(figure)

    with churn_right:
        figure = bar_figure(
            region_churn,
            "Churn Rate by Region",
            "Churn Rate (%)",
            BLUE,
            horizontal=True,
        )
        st.pyplot(figure, width="stretch")
        plt.close(figure)

        figure = bar_figure(
            payment_churn,
            "Churn Rate by Payment Method",
            "Churn Rate (%)",
            AMBER,
        )
        st.pyplot(figure, width="stretch")
        plt.close(figure)

        login_by_status = df.groupby("churned")["last_login_days"].mean()
        login_by_status.index = login_by_status.index.map({0: "Active", 1: "Churned"})
        figure = bar_figure(
            login_by_status,
            "Average Days Since Last Login",
            "Average Days",
            NAVY,
        )
        st.pyplot(figure, width="stretch")
        plt.close(figure)


with questions_tab:
    section_heading(
        "30 Business Questions",
        "Select a question to review its business purpose, course-level Python code, calculated result, and Matplotlib visual.",
    )

    selected_number = st.selectbox(
        "Select a business question",
        list(QUESTIONS.keys()),
        format_func=lambda number: f"Question {number:02d} — {QUESTIONS[number]['title_en']}",
    )
    selected_question = QUESTIONS[selected_number]
    selected_result = run_question(df, selected_number)

    st.markdown(f"### Question {selected_number:02d}")
    st.markdown(f"#### {selected_question['title_en']}")
    st.caption("The result is calculated from the customer segment selected in the sidebar.")

    context_left, context_right = st.columns(2)
    with context_left:
        st.markdown(
            f"""
            <div class="question-context">
                <strong>Business Objective</strong>
                <span>{escape(selected_question['objective'])}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with context_right:
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

    code_column, result_column = st.columns([1.08, 1])
    with code_column:
        st.markdown("#### Analysis Code")
        st.code(QUESTION_CODE[selected_number], language="python", line_numbers=True)
    with result_column:
        st.markdown("#### Calculated Result")
        output_table = result_table(selected_result, selected_number)
        st.dataframe(output_table.round(2), width="stretch", hide_index=True)

    st.markdown("#### Visual Analysis")
    question_figure = create_question_figure(df, selected_number, selected_result)
    st.pyplot(question_figure, width="stretch")
    plt.close(question_figure)


with data_tab:
    section_heading(
        "Data Explorer",
        "Inspect the filtered records, review data quality, and export the current customer segment.",
    )

    data_metric_columns = st.columns(4)
    data_metric_columns[0].metric("Rows", f"{df.shape[0]:,}", border=True)
    data_metric_columns[1].metric("Columns", f"{df.shape[1]}", border=True)
    data_metric_columns[2].metric(
        "Missing Values",
        f"{int(df.isnull().sum().sum()):,}",
        border=True,
    )
    data_metric_columns[3].metric(
        "Duplicate Rows",
        f"{int(df.duplicated().sum()):,}",
        border=True,
    )

    st.markdown("#### Customer Records")
    st.caption("Showing up to the first 100 rows from the current filtered view.")
    st.dataframe(df.head(100), width="stretch", hide_index=True)

    with st.expander("View Descriptive Statistics"):
        st.dataframe(df.describe().round(2), width="stretch")

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Filtered Data",
        data=csv_data,
        file_name="filtered_netflix_customer_churn.csv",
        mime="text/csv",
        width="stretch",
    )


st.markdown(
    '<div class="footer-note">Netflix Customer Churn Analytics • Built with Pandas, NumPy, Matplotlib, and Streamlit</div>',
    unsafe_allow_html=True,
)
