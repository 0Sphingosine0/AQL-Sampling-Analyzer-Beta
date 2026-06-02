import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AQL Sampling Analyzer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# FRUTIGER AERO CSS — LIGHT, GLOSSY, SKY BLUE
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Nunito+Sans:wght@300;400;600;700&display=swap');

/* ══════════════════════════════════════════
   ROOT COLORS — authentic Frutiger Aero
══════════════════════════════════════════ */
:root {
    --sky-top:      #7ec8e3;
    --sky-mid:      #b8e4f7;
    --sky-pale:     #dff2fc;
    --grass:        #c2e8c4;
    --grass-deep:   #8ecf91;
    --white-glass:  rgba(255,255,255,0.72);
    --white-rim:    rgba(255,255,255,0.95);
    --blue-rim:     rgba(80,170,220,0.35);
    --text-dark:    #1a3a52;
    --text-mid:     #2e6a8a;
    --text-soft:    #5a9ab5;
    --accent-blue:  #1e90d4;
    --accent-green: #2aab50;
    --danger:       #d63031;
    --warn:         #e67e22;
}

/* ══════════════════════════════════════════
   BACKGROUND — sky gradient like Windows 7
══════════════════════════════════════════ */
.stApp {
    background:
        radial-gradient(ellipse at 20% 0%, rgba(255,255,255,0.6) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 10%, rgba(180,230,255,0.5) 0%, transparent 45%),
        linear-gradient(180deg,
            #6bbedd 0%,
            #9dd5ef 18%,
            #c8eafa 35%,
            #ddf4fb 50%,
            #e4f7eb 68%,
            #caecd0 85%,
            #b5e3bc 100%
        ) !important;
    background-attachment: fixed !important;
    color: var(--text-dark) !important;
    font-family: 'Nunito Sans', 'Segoe UI', sans-serif;
}

/* Floating bokeh bubbles */
.stApp::before {
    content: '';
    position: fixed;
    top: 5%; left: 8%;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%,
        rgba(255,255,255,0.55) 0%,
        rgba(180,230,255,0.25) 50%,
        transparent 70%);
    border: 1px solid rgba(255,255,255,0.6);
    pointer-events: none;
    z-index: 0;
    animation: float1 12s ease-in-out infinite alternate;
}
.stApp::after {
    content: '';
    position: fixed;
    top: 30%; right: 5%;
    width: 120px; height: 120px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%,
        rgba(255,255,255,0.5) 0%,
        rgba(160,220,245,0.2) 50%,
        transparent 70%);
    border: 1px solid rgba(255,255,255,0.55);
    pointer-events: none;
    z-index: 0;
    animation: float2 16s ease-in-out infinite alternate;
}
@keyframes float1 {
    from { transform: translate(0,0) scale(1); }
    to   { transform: translate(15px, -20px) scale(1.05); }
}
@keyframes float2 {
    from { transform: translate(0,0) scale(1); }
    to   { transform: translate(-12px, 18px) scale(0.95); }
}

/* ══════════════════════════════════════════
   HEADER
══════════════════════════════════════════ */
.app-header {
    background: linear-gradient(160deg,
        rgba(255,255,255,0.82) 0%,
        rgba(210,240,255,0.75) 50%,
        rgba(200,235,215,0.70) 100%);
    border: 1.5px solid var(--white-rim);
    border-top: 2px solid rgba(255,255,255,1);
    border-radius: 20px;
    padding: 28px 36px 24px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(16px);
    box-shadow:
        0 8px 32px rgba(80,160,220,0.18),
        0 2px 8px rgba(255,255,255,0.9),
        inset 0 1px 0 rgba(255,255,255,1);
}
/* glossy shine strip on top */
.app-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 45%;
    background: linear-gradient(180deg,
        rgba(255,255,255,0.55) 0%,
        rgba(255,255,255,0.0) 100%);
    border-radius: 20px 20px 0 0;
    pointer-events: none;
}
.app-title {
    font-family: 'Nunito', sans-serif;
    font-size: 2.5rem;
    font-weight: 900;
    color: #1565a8;
    letter-spacing: 1.5px;
    margin: 0;
    text-shadow:
        0 1px 0 rgba(255,255,255,0.9),
        0 2px 8px rgba(80,160,220,0.25);
}
.app-subtitle {
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text-soft);
    margin-top: 5px;
    letter-spacing: 0.8px;
}
.header-badge {
    display: inline-block;
    background: linear-gradient(135deg,
        rgba(255,255,255,0.9) 0%,
        rgba(200,240,255,0.8) 100%);
    border: 1px solid rgba(100,180,230,0.5);
    border-radius: 20px;
    padding: 3px 16px;
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--accent-blue);
    letter-spacing: 1.5px;
    margin-top: 10px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.9);
}

/* ══════════════════════════════════════════
   METRIC CARDS — glossy white
══════════════════════════════════════════ */
.metric-card {
    background: linear-gradient(175deg,
        rgba(255,255,255,0.90) 0%,
        rgba(220,244,255,0.80) 55%,
        rgba(200,238,255,0.75) 100%);
    border: 1.5px solid rgba(255,255,255,0.95);
    border-bottom: 1.5px solid rgba(160,210,240,0.4);
    border-radius: 16px;
    padding: 20px 16px;
    text-align: center;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
    box-shadow:
        0 4px 16px rgba(80,160,220,0.14),
        0 1px 4px rgba(255,255,255,0.9),
        inset 0 1px 0 rgba(255,255,255,1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow:
        0 10px 28px rgba(80,160,220,0.22),
        inset 0 1px 0 rgba(255,255,255,1);
}
/* glossy top shine */
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 50%;
    background: linear-gradient(180deg,
        rgba(255,255,255,0.7) 0%,
        rgba(255,255,255,0.0) 100%);
    border-radius: 16px 16px 0 0;
    pointer-events: none;
}
.metric-value {
    font-family: 'Nunito', sans-serif;
    font-size: 2.2rem;
    font-weight: 900;
    color: #1565a8;
    line-height: 1.1;
    text-shadow: 0 1px 0 rgba(255,255,255,0.9);
}
.metric-label {
    font-size: 0.70rem;
    font-weight: 700;
    color: var(--text-soft);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 6px;
}

/* ══════════════════════════════════════════
   RESULT BADGES
══════════════════════════════════════════ */
.result-pass {
    background: linear-gradient(160deg,
        rgba(255,255,255,0.88) 0%,
        rgba(210,248,220,0.82) 100%);
    border: 1.5px solid rgba(255,255,255,0.95);
    border-left: 4px solid #2aab50;
    border-radius: 16px;
    padding: 22px 30px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 6px 24px rgba(42,171,80,0.15),
        inset 0 1px 0 rgba(255,255,255,1);
}
.result-pass::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 50%;
    background: linear-gradient(180deg, rgba(255,255,255,0.6) 0%, transparent 100%);
    border-radius: 16px 16px 0 0;
}
.result-pass-text {
    font-family: 'Nunito', sans-serif;
    font-size: 1.9rem;
    font-weight: 900;
    color: #187a2f;
    letter-spacing: 1.5px;
    text-shadow: 0 1px 0 rgba(255,255,255,0.9);
}
.result-fail {
    background: linear-gradient(160deg,
        rgba(255,255,255,0.88) 0%,
        rgba(255,218,210,0.80) 100%);
    border: 1.5px solid rgba(255,255,255,0.95);
    border-left: 4px solid #d63031;
    border-radius: 16px;
    padding: 22px 30px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 6px 24px rgba(214,48,49,0.13),
        inset 0 1px 0 rgba(255,255,255,1);
}
.result-fail::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 50%;
    background: linear-gradient(180deg, rgba(255,255,255,0.6) 0%, transparent 100%);
    border-radius: 16px 16px 0 0;
}
.result-fail-text {
    font-family: 'Nunito', sans-serif;
    font-size: 1.9rem;
    font-weight: 900;
    color: #a01010;
    letter-spacing: 1.5px;
    text-shadow: 0 1px 0 rgba(255,255,255,0.9);
}
.result-sub {
    font-size: 0.92rem;
    color: var(--text-mid);
    margin-top: 8px;
    font-weight: 600;
}

/* ══════════════════════════════════════════
   SECTION TITLE
══════════════════════════════════════════ */
.section-title {
    font-family: 'Nunito', sans-serif;
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--text-dark);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 28px 0 14px 0;
}
.section-title::before {
    content: '';
    display: inline-block;
    width: 5px; height: 18px;
    border-radius: 3px;
    background: linear-gradient(180deg, #5ec8f0, #1e90d4);
    box-shadow: 0 2px 8px rgba(30,144,212,0.4);
    flex-shrink: 0;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(30,144,212,0.3), transparent);
}

/* ══════════════════════════════════════════
   SIDEBAR — frosted white panel
══════════════════════════════════════════ */
div[data-testid="stSidebar"] {
    background: linear-gradient(180deg,
        rgba(255,255,255,0.88) 0%,
        rgba(220,244,255,0.82) 100%) !important;
    border-right: 1.5px solid rgba(255,255,255,0.9) !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 4px 0 20px rgba(80,160,220,0.10) !important;
}
div[data-testid="stSidebar"] * {
    color: var(--text-dark) !important;
}
div[data-testid="stSidebar"] h3 {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    color: #1565a8 !important;
    letter-spacing: 0.5px !important;
}

/* ══════════════════════════════════════════
   INPUTS — glossy white fields
══════════════════════════════════════════ */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background: linear-gradient(180deg,
        rgba(255,255,255,0.95) 0%,
        rgba(235,248,255,0.90) 100%) !important;
    border: 1.5px solid rgba(130,195,230,0.6) !important;
    color: var(--text-dark) !important;
    border-radius: 10px !important;
    box-shadow: inset 0 2px 4px rgba(80,140,180,0.08), 0 1px 0 rgba(255,255,255,1) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div:focus-within,
.stTextInput > div > div:focus-within {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 3px rgba(30,144,212,0.15), inset 0 2px 4px rgba(80,140,180,0.08) !important;
}

/* ══════════════════════════════════════════
   BUTTON — Vista/Win7 glossy pill
══════════════════════════════════════════ */
.stButton > button {
    background:
        linear-gradient(180deg,
            rgba(255,255,255,0.55) 0%,
            rgba(255,255,255,0.0) 50%,
            rgba(0,0,0,0.0) 50%,
            rgba(0,0,0,0.04) 100%),
        linear-gradient(180deg,
            #4ab8e8 0%,
            #1e90d4 48%,
            #1878bc 52%,
            #3aacdc 100%) !important;
    color: #ffffff !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.9rem !important;
    letter-spacing: 1.5px !important;
    border: 1px solid #1268a8 !important;
    border-bottom: 1px solid #0e5490 !important;
    border-radius: 9999px !important;
    padding: 10px 28px !important;
    text-transform: uppercase !important;
    text-shadow: 0 1px 2px rgba(0,60,120,0.5) !important;
    box-shadow:
        0 4px 12px rgba(30,100,200,0.3),
        0 1px 0 rgba(255,255,255,0.4) inset,
        0 -1px 0 rgba(0,0,0,0.15) inset !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow:
        0 8px 20px rgba(30,100,200,0.38),
        0 1px 0 rgba(255,255,255,0.45) inset !important;
    background:
        linear-gradient(180deg,
            rgba(255,255,255,0.6) 0%,
            rgba(255,255,255,0.0) 50%,
            rgba(0,0,0,0.0) 50%,
            rgba(0,0,0,0.04) 100%),
        linear-gradient(180deg,
            #5ec8f5 0%,
            #28a0e8 48%,
            #1e88cc 52%,
            #48bce8 100%) !important;
}
.stButton > button:active {
    transform: translateY(1px) !important;
    box-shadow: 0 2px 6px rgba(30,100,200,0.25) !important;
}

/* ══════════════════════════════════════════
   TABS
══════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.60) !important;
    border-radius: 14px !important;
    padding: 4px 4px !important;
    border: 1.5px solid rgba(255,255,255,0.9) !important;
    box-shadow: 0 2px 8px rgba(80,160,220,0.12), inset 0 1px 0 rgba(255,255,255,1) !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px !important;
    color: var(--text-soft) !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    transition: all 0.2s !important;
    border: none !important;
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255,255,255,0.7) !important;
    color: var(--text-dark) !important;
}
.stTabs [aria-selected="true"] {
    background:
        linear-gradient(180deg,
            rgba(255,255,255,0.9) 0%,
            rgba(200,238,255,0.85) 100%) !important;
    color: #1565a8 !important;
    border: 1px solid rgba(150,210,240,0.5) !important;
    box-shadow:
        0 2px 8px rgba(80,160,220,0.18),
        inset 0 1px 0 rgba(255,255,255,1) !important;
}

/* ══════════════════════════════════════════
   DATAFRAME & MISC
══════════════════════════════════════════ */
.stDataFrame {
    border: 1.5px solid rgba(255,255,255,0.9) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 16px rgba(80,160,220,0.12) !important;
}

.stInfo, .stWarning, .stSuccess {
    border-radius: 12px !important;
    backdrop-filter: blur(8px) !important;
}

h1, h2, h3, h4, h5, h6 {
    color: var(--text-dark) !important;
    font-family: 'Nunito', sans-serif !important;
}
p, span { color: var(--text-dark); }
.stMarkdown p { color: var(--text-mid) !important; }

hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(30,144,212,0.25), transparent) !important;
    margin: 16px 0 !important;
}

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(180deg,
        rgba(255,255,255,0.9) 0%,
        rgba(220,245,255,0.85) 100%) !important;
    border: 1.5px solid rgba(100,180,230,0.6) !important;
    border-radius: 9999px !important;
    color: var(--accent-blue) !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: 1px !important;
    box-shadow: 0 2px 8px rgba(80,160,220,0.15), inset 0 1px 0 rgba(255,255,255,1) !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    box-shadow: 0 6px 18px rgba(80,160,220,0.25), inset 0 1px 0 rgba(255,255,255,1) !important;
    transform: translateY(-1px) !important;
}

.stCaption { color: var(--text-soft) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# AQL DATA TABLES (ISO 2859-1)
# ─────────────────────────────────────────────
LOT_SIZE_TABLE = [
    (2, 8, 'A'), (9, 15, 'B'), (16, 25, 'C'), (26, 50, 'D'),
    (51, 90, 'E'), (91, 150, 'F'), (151, 280, 'G'), (281, 500, 'H'),
    (501, 1200, 'J'), (1201, 3200, 'K'), (3201, 10000, 'L'),
    (10001, 35000, 'M'), (35001, 150000, 'N'), (150001, 500000, 'P'),
    (500001, float('inf'), 'Q'),
]
SAMPLE_SIZE = {
    'A': 2, 'B': 3, 'C': 5, 'D': 8, 'E': 13,
    'F': 20, 'G': 32, 'H': 50, 'J': 80, 'K': 125,
    'L': 200, 'M': 315, 'N': 500, 'P': 800, 'Q': 1250,
}
AQL_TABLE = {
    'A': {0.065:(0,1),0.1:(0,1),0.15:(0,1),0.25:(0,1),0.40:(0,1),0.65:(0,1),1.0:(0,1),1.5:(0,1),2.5:(0,1),4.0:(0,1),6.5:(0,1),10:(0,1)},
    'B': {0.065:(0,1),0.1:(0,1),0.15:(0,1),0.25:(0,1),0.40:(0,1),0.65:(0,1),1.0:(0,1),1.5:(0,1),2.5:(0,1),4.0:(0,1),6.5:(0,1),10:(0,1)},
    'C': {0.065:(0,1),0.1:(0,1),0.15:(0,1),0.25:(0,1),0.40:(0,1),0.65:(0,1),1.0:(0,1),1.5:(0,1),2.5:(0,1),4.0:(0,1),6.5:(1,2),10:(1,2)},
    'D': {0.065:(0,1),0.1:(0,1),0.15:(0,1),0.25:(0,1),0.40:(0,1),0.65:(0,1),1.0:(0,1),1.5:(0,1),2.5:(0,1),4.0:(1,2),6.5:(1,2),10:(2,3)},
    'E': {0.065:(0,1),0.1:(0,1),0.15:(0,1),0.25:(0,1),0.40:(0,1),0.65:(0,1),1.0:(0,1),1.5:(0,1),2.5:(1,2),4.0:(1,2),6.5:(2,3),10:(3,4)},
    'F': {0.065:(0,1),0.1:(0,1),0.15:(0,1),0.25:(0,1),0.40:(0,1),0.65:(0,1),1.0:(0,1),1.5:(1,2),2.5:(1,2),4.0:(2,3),6.5:(3,4),10:(5,6)},
    'G': {0.065:(0,1),0.1:(0,1),0.15:(0,1),0.25:(0,1),0.40:(0,1),0.65:(1,2),1.0:(1,2),1.5:(1,2),2.5:(2,3),4.0:(3,4),6.5:(5,6),10:(7,8)},
    'H': {0.065:(0,1),0.1:(0,1),0.15:(0,1),0.25:(0,1),0.40:(1,2),0.65:(1,2),1.0:(1,2),1.5:(2,3),2.5:(3,4),4.0:(5,6),6.5:(7,8),10:(10,11)},
    'J': {0.065:(0,1),0.1:(0,1),0.15:(0,1),0.25:(1,2),0.40:(1,2),0.65:(2,3),1.0:(2,3),1.5:(3,4),2.5:(5,6),4.0:(7,8),6.5:(10,11),10:(14,15)},
    'K': {0.065:(0,1),0.1:(0,1),0.15:(1,2),0.25:(1,2),0.40:(2,3),0.65:(3,4),1.0:(3,4),1.5:(5,6),2.5:(7,8),4.0:(10,11),6.5:(14,15),10:(21,22)},
    'L': {0.065:(0,1),0.1:(1,2),0.15:(1,2),0.25:(2,3),0.40:(3,4),0.65:(5,6),1.0:(5,6),1.5:(7,8),2.5:(10,11),4.0:(14,15),6.5:(21,22),10:(21,22)},
    'M': {0.065:(1,2),0.1:(1,2),0.15:(2,3),0.25:(3,4),0.40:(5,6),0.65:(7,8),1.0:(7,8),1.5:(10,11),2.5:(14,15),4.0:(21,22),6.5:(21,22),10:(21,22)},
    'N': {0.065:(1,2),0.1:(2,3),0.15:(3,4),0.25:(5,6),0.40:(7,8),0.65:(10,11),1.0:(10,11),1.5:(14,15),2.5:(21,22),4.0:(21,22),6.5:(21,22),10:(21,22)},
    'P': {0.065:(2,3),0.1:(3,4),0.15:(5,6),0.25:(7,8),0.40:(10,11),0.65:(14,15),1.0:(14,15),1.5:(21,22),2.5:(21,22),4.0:(21,22),6.5:(21,22),10:(21,22)},
    'Q': {0.065:(3,4),0.1:(5,6),0.15:(7,8),0.25:(10,11),0.40:(14,15),0.65:(21,22),1.0:(21,22),1.5:(21,22),2.5:(21,22),4.0:(21,22),6.5:(21,22),10:(21,22)},
}
AQL_LEVELS = [0.065, 0.1, 0.15, 0.25, 0.40, 0.65, 1.0, 1.5, 2.5, 4.0, 6.5, 10]

def get_code_letter(lot_size):
    for low, high, code in LOT_SIZE_TABLE:
        if low <= lot_size <= high:
            return code
    return 'Q'

def get_aql_criteria(code_letter, aql):
    return AQL_TABLE.get(code_letter, {}).get(aql, None)

def get_defect_rate(n_defects, sample_size):
    return (n_defects / sample_size) * 100 if sample_size > 0 else 0

# ─────────────────────────────────────────────
# PLOTLY THEME — light, airy, Frutiger
# ─────────────────────────────────────────────
PAPER_BG    = 'rgba(230,248,255,0.7)'
PLOT_BG     = 'rgba(245,252,255,0.5)'
GRID_COLOR  = 'rgba(100,180,220,0.18)'
TICK_COLOR  = '#4a90b8'
BLUE_LINE   = '#1e90d4'
GREEN_LINE  = '#2aab50'
DANGER_LINE = '#d63031'
GOLD_LINE   = '#e67e22'
FONT_FAM    = 'Nunito, Segoe UI, sans-serif'

def aero_layout(**kw):
    base = dict(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color='#1a3a52', family=FONT_FAM, size=12),
        margin=dict(l=24, r=24, t=44, b=24),
        xaxis=dict(gridcolor=GRID_COLOR, tickcolor=TICK_COLOR,
                   linecolor='rgba(100,180,220,0.3)', color=TICK_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, tickcolor=TICK_COLOR,
                   linecolor='rgba(100,180,220,0.3)', color=TICK_COLOR),
    )
    base.update(kw)
    return base

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="app-title">🔬 AQL Sampling Analyzer</div>
    <div class="app-subtitle">Pengolahan Data Sampling &amp; Acceptance Quality Limit · ISO 2859-1</div>
    <div class="header-badge">✦ KELOMPOK 7 · LPK 2026 ✦</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Parameter Sampling")
    st.markdown("---")
    lot_size = st.number_input("Ukuran Lot (Batch)", min_value=2, max_value=999999, value=1000, step=50)
    aql_level = st.selectbox("AQL Level (%)", options=AQL_LEVELS, index=6, format_func=lambda x: f"{x}%")
    inspection_type = st.selectbox("Tipe Inspeksi", ["Normal", "Ketat (Tightened)", "Longgar (Reduced)"])
    st.markdown("---")
    st.markdown("### 📥 Data Defek")
    n_defects = st.number_input("Jumlah Defek Ditemukan", min_value=0, max_value=9999, value=3)
    st.markdown("---")
    st.markdown("### 📋 Info Lot")
    product_name = st.text_input("Nama Produk/Lot", value="Sampel Kimia A")
    lot_number   = st.text_input("Nomor Lot", value="LOT-2026-001")
    inspector    = st.text_input("Nama Inspektor", value="Kelompok 7")
    analyze_btn  = st.button("🔍 ANALISIS SEKARANG", use_container_width=True)

# ─────────────────────────────────────────────
# CALCULATION
# ─────────────────────────────────────────────
code_letter   = get_code_letter(lot_size)
sample_size   = SAMPLE_SIZE.get(code_letter, 2)
criteria      = get_aql_criteria(code_letter, aql_level)
ac, re        = criteria if criteria else (0, 1)
defect_rate   = get_defect_rate(n_defects, sample_size)
decision_pass = n_defects <= ac

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Hasil Analisis", "📈 Visualisasi", "📋 Tabel AQL", "📄 Laporan"])

# ── TAB 1 ────────────────────────────────────
with tab1:
    st.markdown('<div class="section-title">Parameter Lot</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl in zip(
        [c1, c2, c3, c4],
        [f"{lot_size:,}", code_letter, str(sample_size), f"{aql_level}%"],
        ["Ukuran Lot", "Kode Sampel", "Ukuran Sampel", "AQL Level"]
    ):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Kriteria Penerimaan</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl in zip(
        [c1, c2, c3, c4],
        [str(ac), str(re), str(n_defects), f"{defect_rate:.2f}%"],
        ["Accept Number (Ac)", "Reject Number (Re)", "Defek Ditemukan", "Defect Rate"]
    ):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Keputusan Sampling</div>', unsafe_allow_html=True)
    if decision_pass:
        st.markdown(f"""
        <div class="result-pass">
            <div class="result-pass-text">✅ LOT DITERIMA (ACCEPT)</div>
            <div class="result-sub">Defek ({n_defects}) ≤ Ac ({ac}) — Lot memenuhi standar AQL {aql_level}%</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-fail">
            <div class="result-fail-text">❌ LOT DITOLAK (REJECT)</div>
            <div class="result-sub">Defek ({n_defects}) ≥ Re ({re}) — Lot tidak memenuhi standar AQL {aql_level}%</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="section-title">Interpretasi</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.info(f"""
**📌 Tentang Lot Ini**
- **Produk:** {product_name}
- **Nomor Lot:** {lot_number}
- **Inspektor:** {inspector}
- **Tipe Inspeksi:** {inspection_type}
        """)
    with col_b:
        sampling_ratio = (sample_size / lot_size) * 100
        rekomendasi = (
            "✅ Lot dapat dikirim/digunakan. Lanjutkan proses produksi normal."
            if decision_pass else
            "❌ Lakukan inspeksi 100% atau kembalikan ke supplier. Tinjau proses produksi."
        )
        st.warning(f"""
**💡 Rekomendasi Tindakan**

{rekomendasi}

- Rasio sampling: **{sampling_ratio:.1f}%** dari lot
- Confidence level: **~95%** (General Inspection Level II)
        """)

# ── TAB 2 ────────────────────────────────────
with tab2:
    st.markdown('<div class="section-title">Visualisasi Data Sampling</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    # Gauge
    with col1:
        gc = GREEN_LINE if decision_pass else DANGER_LINE
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=n_defects,
            delta={'reference': ac, 'increasing': {'color': DANGER_LINE}, 'decreasing': {'color': GREEN_LINE}},
            title={'text': "Jumlah Defek vs Accept Number", 'font': {'color': '#1a3a52', 'family': FONT_FAM, 'size': 14}},
            gauge={
                'axis': {'range': [0, max(re*2, n_defects*1.5, 5)], 'tickcolor': TICK_COLOR},
                'bar': {'color': gc, 'thickness': 0.25},
                'bgcolor': 'rgba(220,245,255,0.6)',
                'borderwidth': 1, 'bordercolor': 'rgba(100,180,220,0.4)',
                'steps': [
                    {'range': [0, ac],                           'color': 'rgba(42,171,80,0.12)'},
                    {'range': [ac, re],                          'color': 'rgba(230,126,34,0.12)'},
                    {'range': [re, max(re*2,n_defects*1.5,5)],  'color': 'rgba(214,48,49,0.12)'},
                ],
                'threshold': {'line': {'color': DANGER_LINE, 'width': 2}, 'thickness': 0.75, 'value': re}
            },
            number={'font': {'color': gc, 'family': FONT_FAM, 'size': 38}}
        ))
        fig_gauge.update_layout(**aero_layout(height=320))
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Donut
    with col2:
        good = max(sample_size - n_defects, 0)
        fig_pie = go.Figure(go.Pie(
            labels=['Baik', 'Defek'], values=[good, n_defects], hole=0.58,
            marker=dict(colors=[BLUE_LINE, DANGER_LINE], line=dict(color='rgba(255,255,255,0.8)', width=2)),
            textfont=dict(family=FONT_FAM, size=13, color='#1a3a52'),
        ))
        fig_pie.update_layout(**aero_layout(
            height=320,
            title=dict(text='Komposisi Sampel', font=dict(family=FONT_FAM, color='#1a3a52', size=14)),
            legend=dict(font=dict(color='#1a3a52'))
        ))
        st.plotly_chart(fig_pie, use_container_width=True)

    # Sensitivity bar
    st.markdown('<div class="section-title">Analisis Sensitivitas — Keputusan per Jumlah Defek</div>', unsafe_allow_html=True)
    max_def = max(re * 3, 10)
    defect_range = list(range(0, max_def + 1))
    colors_bar = [GREEN_LINE if d <= ac else DANGER_LINE for d in defect_range]
    fig_bar = go.Figure(go.Bar(
        x=defect_range, y=defect_range,
        marker=dict(color=colors_bar, line=dict(color='rgba(255,255,255,0.6)', width=1)),
        text=['ACCEPT' if d <= ac else 'REJECT' for d in defect_range],
        textposition='auto',
        textfont=dict(family=FONT_FAM, size=10, color='#ffffff'),
    ))
    fig_bar.add_vline(x=ac+0.5, line_color=GOLD_LINE, line_dash='dash', line_width=1.5,
                      annotation_text=f'Batas Ac={ac}', annotation_font_color=GOLD_LINE)
    fig_bar.update_layout(**aero_layout(
        height=280, showlegend=False,
        xaxis=dict(title='Jumlah Defek', gridcolor=GRID_COLOR, tickcolor=TICK_COLOR, color=TICK_COLOR),
        yaxis=dict(title='Jumlah Defek', gridcolor=GRID_COLOR, tickcolor=TICK_COLOR, color=TICK_COLOR),
    ))
    st.plotly_chart(fig_bar, use_container_width=True)

    # OC Curve
    st.markdown('<div class="section-title">OC Curve — Kurva Karakteristik Operasi</div>', unsafe_allow_html=True)
    p_values  = np.linspace(0, 0.3, 200)
    pa_values = [sum(math.comb(sample_size, k)*(p**k)*((1-p)**(sample_size-k)) for k in range(ac+1))*100
                 for p in p_values]
    fig_oc = go.Figure()
    fig_oc.add_trace(go.Scatter(
        x=p_values*100, y=pa_values, mode='lines', name='P(Accept)',
        line=dict(color=BLUE_LINE, width=2.5),
        fill='tozeroy', fillcolor='rgba(30,144,212,0.08)'
    ))
    fig_oc.add_vline(x=aql_level, line_color=GOLD_LINE, line_dash='dot',
                     annotation_text=f'AQL={aql_level}%', annotation_font_color=GOLD_LINE)
    fig_oc.add_hline(y=95, line_color='rgba(100,180,220,0.5)', line_dash='dot',
                     annotation_text='95%', annotation_font_color=TICK_COLOR)
    fig_oc.update_layout(**aero_layout(
        height=300,
        xaxis=dict(title='Defect Rate (%)', gridcolor=GRID_COLOR, tickcolor=TICK_COLOR, color=TICK_COLOR),
        yaxis=dict(title='P(Accept) %', gridcolor=GRID_COLOR, tickcolor=TICK_COLOR, color=TICK_COLOR, range=[0,105]),
        legend=dict(font=dict(color='#1a3a52'))
    ))
    st.plotly_chart(fig_oc, use_container_width=True)

# ── TAB 3 ────────────────────────────────────
with tab3:
    st.markdown('<div class="section-title">Tabel Referensi AQL (ISO 2859-1 — Normal Inspection)</div>', unsafe_allow_html=True)
    rows = []
    for low, high, code in LOT_SIZE_TABLE:
        n   = SAMPLE_SIZE[code]
        row = {'Ukuran Lot': f"{low:,} – {high:,}" if high != float('inf') else f"≥ {low:,}",
               'Kode': code, 'n Sampel': n}
        for aql_v in [0.65, 1.0, 1.5, 2.5, 4.0, 6.5]:
            crit = AQL_TABLE[code].get(aql_v, (0,1))
            row[f'AQL {aql_v}%'] = f"Ac={crit[0]}  Re={crit[1]}"
        rows.append(row)
    df_table = pd.DataFrame(rows)

    def highlight_current(row):
        if row['Kode'] == code_letter:
            return ['background-color: rgba(30,144,212,0.12); color: #1565a8; font-weight: bold'] * len(row)
        return [''] * len(row)

    st.dataframe(df_table.style.apply(highlight_current, axis=1), use_container_width=True, height=420)
    st.caption(f"🔵 Baris yang di-highlight = kode {code_letter} sesuai lot size {lot_size:,}")

    st.markdown('<div class="section-title">Tabel Ukuran Lot → Kode Sampel</div>', unsafe_allow_html=True)
    st.markdown("""
| Ukuran Lot | Kode | n Sampel | Ukuran Lot | Kode | n Sampel |
|---|---|---|---|---|---|
| 2–8 | A | 2 | 501–1,200 | J | 80 |
| 9–15 | B | 3 | 1,201–3,200 | K | 125 |
| 16–25 | C | 5 | 3,201–10,000 | L | 200 |
| 26–50 | D | 8 | 10,001–35,000 | M | 315 |
| 51–90 | E | 13 | 35,001–150,000 | N | 500 |
| 91–150 | F | 20 | 150,001–500,000 | P | 800 |
| 151–280 | G | 32 | ≥ 500,001 | Q | 1,250 |
| 281–500 | H | 50 | | | |
""")

# ── TAB 4 ────────────────────────────────────
with tab4:
    st.markdown('<div class="section-title">Laporan Hasil Sampling</div>', unsafe_allow_html=True)
    from datetime import datetime
    now = datetime.now().strftime("%d %B %Y, %H:%M")
    report_text = f"""
## 📄 LAPORAN HASIL SAMPLING AQL
**Tanggal:** {now}

---

### Identifikasi Lot
| Parameter | Nilai |
|---|---|
| Nama Produk | {product_name} |
| Nomor Lot | {lot_number} |
| Inspektor | {inspector} |
| Tipe Inspeksi | {inspection_type} |

### Parameter Sampling (ISO 2859-1)
| Parameter | Nilai |
|---|---|
| Ukuran Lot | {lot_size:,} unit |
| Kode Sampel | {code_letter} |
| Ukuran Sampel (n) | {sample_size} unit |
| AQL Level | {aql_level}% |
| Accept Number (Ac) | {ac} |
| Reject Number (Re) | {re} |

### Hasil Pemeriksaan
| Parameter | Nilai |
|---|---|
| Jumlah Defek Ditemukan | {n_defects} unit |
| Defect Rate | {defect_rate:.3f}% |
| Keputusan | **{"ACCEPT ✅" if decision_pass else "REJECT ❌"}** |

### Dasar Keputusan
{"Lot **DITERIMA** karena jumlah defek (" + str(n_defects) + ") tidak melebihi Accept Number (" + str(ac) + ") sesuai standar AQL " + str(aql_level) + "%." if decision_pass else "Lot **DITOLAK** karena jumlah defek (" + str(n_defects) + ") mencapai atau melebihi Reject Number (" + str(re) + ") sesuai standar AQL " + str(aql_level) + "%."}

### Rekomendasi
{"✅ Lot dapat diterima dan diteruskan ke proses selanjutnya." if decision_pass else "❌ Lakukan inspeksi 100% atau kembalikan ke supplier."}

---
*AQL Sampling Analyzer — Kelompok 7 LPK 2026 | ISO 2859-1*
    """
    st.markdown(report_text)
    st.download_button(
        label="📥 Unduh Laporan (.txt)",
        data=report_text,
        file_name=f"laporan_aql_{lot_number.replace('-','_')}.txt",
        mime="text/plain",
        use_container_width=True
    )
    st.markdown("---")
    st.markdown("""
<div style="text-align:center; color:#5a9ab5; font-family:'Nunito',sans-serif; letter-spacing:2px; font-size:0.80rem; margin-top:12px; padding:14px; background:rgba(255,255,255,0.5); border-radius:12px; border:1px solid rgba(255,255,255,0.9);">
    AQL SAMPLING ANALYZER &nbsp;·&nbsp; KELOMPOK 7 &nbsp;·&nbsp; LPK 2026<br>
    <span style="opacity:0.6;">Standar: ISO 2859-1 · General Inspection Level II · Single Sampling Normal</span>
</div>
""", unsafe_allow_html=True)
PYEOF
Output

Input validation errors occurred:
description: Field required
Done

You are out of free messages until 12:40 AM
