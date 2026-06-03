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
    page_title="AQL Sampling Analyzer 🎀",
    page_icon="🎀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# OPENING / INTRODUCTION
# ─────────────────────────────────────────────
with st.expander("🎀 TENTANG APLIKASI & KELOMPOK 7 🎀", expanded=True):
    st.markdown("""
    **✿ Selamat Datang di AQL Sampling Analyzer ✿**
    
    Aplikasi ini dirancang sebagai alat bantu interaktif untuk mempermudah proses *Quality Control* (QC) dan pengambilan keputusan dalam penerimaan lot produk. 
    
    **Tujuan & Kegunaan:**
    - Menentukan ukuran sampel (*Sample Size*) secara otomatis berdasarkan jumlah produksi lot/batch.
    - Menetapkan kriteria batas penerimaan (*Acceptance Number/Ac*) dan penolakan (*Rejection Number/Re*).
    - Meminimalisir kesalahan interpretasi tabel manual dan menyediakan laporan serta visualisasi inspeksi atribut yang efisien.
    
    **Sumber Data (Standar Referensi):**
    Seluruh logika kalkulasi dan tabel acuan dalam aplikasi ini merujuk pada **Standar Internasional ISO 2859-1** *(Sampling procedures for inspection by attributes)* untuk inspeksi umum level II (Single Sampling Normal).
    
    **Dikembangkan Oleh Kelompok 7:**
    1. **Iren Nethania Rifai** (2560644)
    2. **Mayang Devani Dwi Nanda** (2560669)
    3. **Putri Anisa** (2560737)
    4. **Shally Ardhany** (2560778)
    5. **Shiela Feriska Demayanti** (2560779)
    """)
    
# ─────────────────────────────────────────────
# COQUETTE CSS 🎀
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Lato:wght@300;400;700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&display=swap');

:root {
    --blush:        #f7c5d0;
    --rose:         #e8a0b0;
    --deep-rose:    #c9748a;
    --petal:        #fde8ee;
    --cream:        #fdf6f8;
    --lavender:     #e8d5f0;
    --lilac:        #d4a8e8;
    --mauve:        #b48aad;
    --ribbon:       #e07090;
    --ribbon-dark:  #c05070;
    --lace:         rgba(247,197,208,0.25);
    --lace-border:  rgba(232,160,176,0.45);
    --text-dark:    #5a2d42;
    --text-mid:     #8a5a6a;
    --text-soft:    #b08090;
    --white-soft:   rgba(255,255,255,0.85);
    --pass-green:   #6ab58a;
    --fail-red:     #d9607a;
    --bg-main: linear-gradient(160deg, #fff0f5 0%, #fde8ee 30%, #f5e0f0 60%, #fce8f5 100%);
}

/* ── GLOBAL ── */
.stApp {
    background: var(--bg-main) !important;
    background-attachment: fixed !important;
    color: var(--text-dark) !important;
    font-family: 'Lato', sans-serif;
}

/* Floating decorative elements */
.stApp::before {
    content: '🎀';
    position: fixed;
    top: 5%;
    right: 3%;
    font-size: 4rem;
    opacity: 0.12;
    animation: float1 6s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}
.stApp::after {
    content: '🌸';
    position: fixed;
    bottom: 8%;
    left: 2%;
    font-size: 5rem;
    opacity: 0.10;
    animation: float2 8s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}
@keyframes float1 { 0%,100%{transform:translateY(0) rotate(-5deg);} 50%{transform:translateY(-12px) rotate(5deg);} }
@keyframes float2 { 0%,100%{transform:translateY(0) rotate(3deg);} 50%{transform:translateY(-16px) rotate(-4deg);} }

/* ── HEADER ── */
.app-header {
    background: linear-gradient(135deg,
        rgba(255,255,255,0.90) 0%,
        rgba(253,232,238,0.85) 50%,
        rgba(248,220,235,0.80) 100%);
    border: 2px solid var(--lace-border);
    border-radius: 24px;
    padding: 36px 44px 30px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow:
        0 8px 40px rgba(232,160,176,0.20),
        inset 0 1px 0 rgba(255,255,255,0.95),
        0 0 0 1px rgba(247,197,208,0.3);
    text-align: center;
}

/* Lace top border decoration */
.app-header::before {
    content: '✿ ❧ 🎀 ❧ ✿ ❧ 🎀 ❧ ✿ ❧ 🎀 ❧ ✿';
    position: absolute;
    top: 8px;
    left: 0; right: 0;
    text-align: center;
    font-size: 0.8rem;
    letter-spacing: 4px;
    color: var(--rose);
    opacity: 0.6;
}
.app-header::after {
    content: '✿ ❧ 🎀 ❧ ✿ ❧ 🎀 ❧ ✿ ❧ 🎀 ❧ ✿';
    position: absolute;
    bottom: 8px;
    left: 0; right: 0;
    text-align: center;
    font-size: 0.8rem;
    letter-spacing: 4px;
    color: var(--rose);
    opacity: 0.6;
}

.app-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 700;
    font-style: italic;
    background: linear-gradient(135deg, var(--ribbon-dark) 0%, var(--deep-rose) 40%, var(--mauve) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 2px;
    margin: 10px 0 0 0;
    filter: drop-shadow(0 2px 6px rgba(201,116,138,0.25));
}
.app-subtitle {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.05rem;
    font-style: italic;
    font-weight: 300;
    color: var(--text-mid);
    margin-top: 8px;
    letter-spacing: 1.5px;
    opacity: 0.9;
}
.header-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(224,112,144,0.15), rgba(212,168,232,0.15));
    border: 1px solid var(--lace-border);
    border-radius: 30px;
    padding: 5px 20px;
    font-size: 0.78rem;
    color: var(--ribbon);
    letter-spacing: 2px;
    margin-top: 12px;
    font-weight: 700;
    font-family: 'Lato', sans-serif;
    text-transform: uppercase;
}

/* ── RIBBON SVG DECORATIONS (inline via pseudo) ── */

/* ── GLASS CARD ── */
.glass-card {
    background: linear-gradient(145deg,
        rgba(255,255,255,0.88) 0%,
        rgba(253,232,238,0.70) 100%);
    border: 1.5px solid var(--lace-border);
    border-radius: 18px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow:
        0 4px 24px rgba(232,160,176,0.15),
        inset 0 1px 0 rgba(255,255,255,0.95);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}
.glass-card:hover {
    transform: translateY(-3px);
    box-shadow:
        0 12px 40px rgba(232,160,176,0.25),
        inset 0 1px 0 rgba(255,255,255,1);
    border-color: var(--ribbon);
}

/* ── METRIC CARDS ── */
.metric-card {
    background: linear-gradient(145deg,
        rgba(255,255,255,0.92) 0%,
        rgba(253,232,238,0.75) 100%);
    border: 1.5px solid var(--lace-border);
    border-radius: 18px;
    padding: 22px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(8px);
    box-shadow:
        0 4px 20px rgba(232,160,176,0.12),
        inset 0 1px 0 rgba(255,255,255,0.95);
    transition: all 0.3s ease;
}
.metric-card::before {
    content: '🎀';
    position: absolute;
    top: 6px;
    right: 8px;
    font-size: 0.9rem;
    opacity: 0.35;
}
.metric-card:hover {
    border-color: var(--ribbon);
    box-shadow:
        0 8px 30px rgba(232,160,176,0.25),
        inset 0 1px 0 rgba(255,255,255,1);
    transform: translateY(-2px);
}
.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--ribbon-dark), var(--mauve));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 1px 4px rgba(201,116,138,0.20));
    line-height: 1.1;
}
.metric-label {
    font-size: 0.70rem;
    color: var(--text-soft);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 6px;
    font-weight: 700;
    font-family: 'Lato', sans-serif;
}

/* ── RESULT BADGES ── */
.result-pass {
    background: linear-gradient(135deg,
        rgba(255,255,255,0.90) 0%,
        rgba(213,240,225,0.70) 100%);
    border: 2px solid rgba(106,181,138,0.55);
    border-radius: 18px;
    padding: 28px 32px;
    text-align: center;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(106,181,138,0.15);
}
.result-pass::before {
    content: '✿ 🌸 ✿ 🌸 ✿ 🌸 ✿ 🌸 ✿';
    position: absolute;
    top: 8px;
    left: 0; right: 0;
    text-align: center;
    font-size: 0.75rem;
    color: var(--pass-green);
    opacity: 0.5;
    letter-spacing: 6px;
}
.result-pass-text {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    font-style: italic;
    background: linear-gradient(135deg, #3a8a5a, #6ab58a);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 1px;
    filter: drop-shadow(0 1px 4px rgba(106,181,138,0.3));
}
.result-fail {
    background: linear-gradient(135deg,
        rgba(255,255,255,0.90) 0%,
        rgba(250,220,228,0.70) 100%);
    border: 2px solid rgba(217,96,122,0.55);
    border-radius: 18px;
    padding: 28px 32px;
    text-align: center;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(217,96,122,0.15);
}
.result-fail::before {
    content: '🥀 ✦ 🥀 ✦ 🥀 ✦ 🥀 ✦ 🥀';
    position: absolute;
    top: 8px;
    left: 0; right: 0;
    text-align: center;
    font-size: 0.75rem;
    color: var(--fail-red);
    opacity: 0.5;
    letter-spacing: 6px;
}
.result-fail-text {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    font-style: italic;
    background: linear-gradient(135deg, var(--ribbon-dark), var(--fail-red));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 1px;
    filter: drop-shadow(0 1px 4px rgba(217,96,122,0.3));
}
.result-sub {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1rem;
    font-style: italic;
    color: var(--text-mid);
    margin-top: 8px;
}

/* ── SECTION TITLE ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 600;
    font-style: italic;
    color: var(--ribbon-dark);
    letter-spacing: 1.5px;
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 28px 0 14px 0;
}
.section-title::before {
    content: '🎀';
    font-size: 1rem;
    flex-shrink: 0;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1.5px;
    background: linear-gradient(90deg, var(--rose), rgba(232,160,176,0.1));
    margin-left: 4px;
}

/* ── SIDEBAR ── */
div[data-testid="stSidebar"] {
    background: linear-gradient(180deg,
        rgba(253,240,245,0.98) 0%,
        rgba(248,230,238,0.98) 100%) !important;
    border-right: 2px solid var(--lace-border) !important;
    backdrop-filter: blur(16px) !important;
}
div[data-testid="stSidebar"]::before {
    content: '🎀 ✿ 🌸 ✿ 🎀 ✿ 🌸 ✿ 🎀';
    position: absolute;
    top: 10px;
    left: 0; right: 0;
    text-align: center;
    font-size: 0.7rem;
    letter-spacing: 3px;
    opacity: 0.35;
    z-index: 1;
    pointer-events: none;
}
div[data-testid="stSidebar"] * { color: var(--text-dark) !important; }
div[data-testid="stSidebar"] h3 {
    font-family: 'Playfair Display', serif !important;
    font-style: italic !important;
    letter-spacing: 1px !important;
    color: var(--ribbon-dark) !important;
}

/* ── FORM INPUTS ── */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.90) !important;
    border: 1.5px solid var(--lace-border) !important;
    color: var(--text-dark) !important;
    border-radius: 12px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    font-family: 'Lato', sans-serif !important;
}
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div:focus-within,
.stTextInput > div > div:focus-within {
    border-color: var(--ribbon) !important;
    box-shadow: 0 0 0 3px rgba(224,112,144,0.15) !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg,
        var(--ribbon) 0%,
        var(--deep-rose) 100%) !important;
    color: #ffffff !important;
    font-family: 'Playfair Display', serif !important;
    font-weight: 700 !important;
    font-style: italic !important;
    font-size: 1rem !important;
    letter-spacing: 2px !important;
    border: 2px solid rgba(255,255,255,0.4) !important;
    border-radius: 30px !important;
    padding: 12px 28px !important;
    transition: all 0.25s ease !important;
    box-shadow:
        0 4px 15px rgba(224,112,144,0.30),
        inset 0 1px 0 rgba(255,255,255,0.35) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::before {
    content: '🎀 ';
    font-style: normal;
}
.stButton > button::after {
    content: ' 🎀';
    font-style: normal;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow:
        0 10px 30px rgba(224,112,144,0.45),
        inset 0 1px 0 rgba(255,255,255,0.45) !important;
    background: linear-gradient(135deg,
        #ec8aaa 0%,
        var(--ribbon) 100%) !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.70) !important;
    border-radius: 14px !important;
    padding: 5px !important;
    border: 1.5px solid var(--lace-border) !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px !important;
    color: var(--text-soft) !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1rem !important;
    font-style: italic !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s !important;
    border: none !important;
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(247,197,208,0.25) !important;
    color: var(--ribbon-dark) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,
        rgba(224,112,144,0.20) 0%,
        rgba(212,168,232,0.15) 100%) !important;
    color: var(--ribbon-dark) !important;
    border: 1.5px solid var(--lace-border) !important;
    box-shadow: 0 2px 10px rgba(224,112,144,0.15) !important;
}

/* ── DATAFRAME ── */
.stDataFrame {
    border: 1.5px solid var(--lace-border) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}

/* ── ALERTS / INFO ── */
.stInfo, .stWarning, .stSuccess, .stError {
    border-radius: 14px !important;
    backdrop-filter: blur(8px) !important;
    font-family: 'Lato', sans-serif !important;
}

/* ── MISC OVERRIDES ── */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-dark) !important;
    font-family: 'Playfair Display', serif !important;
    font-style: italic !important;
}
p, span, label { color: var(--text-dark) !important; }
.stMarkdown p {
    color: var(--text-mid) !important;
    font-family: 'Lato', sans-serif !important;
}

/* Divider */
hr {
    border: none !important;
    height: 1.5px !important;
    background: linear-gradient(90deg, transparent, var(--rose), transparent) !important;
    margin: 16px 0 !important;
}

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(135deg,
        rgba(255,255,255,0.92) 0%,
        rgba(253,232,238,0.80) 100%) !important;
    border: 2px solid var(--lace-border) !important;
    color: var(--ribbon-dark) !important;
    font-family: 'Playfair Display', serif !important;
    font-style: italic !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px !important;
    border-radius: 30px !important;
    transition: all 0.25s !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg,
        rgba(247,197,208,0.40) 0%,
        rgba(212,168,232,0.30) 100%) !important;
    box-shadow: 0 0 20px rgba(224,112,144,0.25) !important;
    transform: translateY(-2px) !important;
    border-color: var(--ribbon) !important;
}

/* Caption */
.stCaption {
    color: var(--text-soft) !important;
    font-style: italic;
    font-family: 'Cormorant Garamond', serif !important;
}

/* Expander */
.streamlit-expanderHeader {
    font-family: 'Playfair Display', serif !important;
    font-style: italic !important;
    color: var(--ribbon-dark) !important;
    background: rgba(255,255,255,0.80) !important;
    border-radius: 12px !important;
    border: 1.5px solid var(--lace-border) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--petal); }
::-webkit-scrollbar-thumb { background: var(--rose); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--ribbon); }

/* Label text */
.stNumberInput label, .stSelectbox label, .stTextInput label {
    color: var(--text-mid) !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-style: italic !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.5px !important;
}
</style>

<!-- Floating ribbon decorations -->
<div style="position:fixed;top:15%;left:1%;font-size:2.5rem;opacity:0.07;transform:rotate(-20deg);pointer-events:none;z-index:0;animation:float1 7s ease-in-out infinite;">🎀</div>
<div style="position:fixed;top:45%;right:0.5%;font-size:2rem;opacity:0.08;transform:rotate(15deg);pointer-events:none;z-index:0;animation:float2 9s ease-in-out infinite;">🌸</div>
<div style="position:fixed;top:70%;left:0.5%;font-size:1.8rem;opacity:0.07;pointer-events:none;z-index:0;animation:float1 11s ease-in-out infinite;">🌷</div>
<style>
@keyframes float1{0%,100%{transform:translateY(0) rotate(-20deg);}50%{transform:translateY(-14px) rotate(-10deg);}}
@keyframes float2{0%,100%{transform:translateY(0) rotate(15deg);}50%{transform:translateY(-18px) rotate(5deg);}}
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
    table = AQL_TABLE.get(code_letter, {})
    return table.get(aql, None)

def get_defect_rate(n_defects, sample_size):
    return (n_defects / sample_size) * 100 if sample_size > 0 else 0

# ─────────────────────────────────────────────
# PLOTLY THEME (Coquette)
# ─────────────────────────────────────────────
PLOT_BG      = 'rgba(253,240,245,0.0)'
PAPER_BG     = 'rgba(253,232,238,0.75)'
GRID_COLOR   = 'rgba(232,160,176,0.20)'
TICK_COLOR   = '#b08090'
ROSE_COLOR   = '#e07090'
LAVENDER_COLOR = '#b48aad'
PASS_COLOR   = '#6ab58a'
FAIL_COLOR   = '#d9607a'
FONT_FAMILY  = 'Lato, sans-serif'

def coquette_layout(**kwargs):
    base = dict(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color='#5a2d42', family=FONT_FAMILY, size=12),
        margin=dict(l=24, r=24, t=40, b=24),
        xaxis=dict(gridcolor=GRID_COLOR, tickcolor=TICK_COLOR, linecolor='rgba(232,160,176,0.3)', color=TICK_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, tickcolor=TICK_COLOR, linecolor='rgba(232,160,176,0.3)', color=TICK_COLOR),
    )
    base.update(kwargs)
    return base

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="app-title">🎀 AQL Sampling Analyzer 🎀</div>
    <div class="app-subtitle">Pengolahan Data Sampling & Acceptance Quality Limit · ISO 2859-1</div>
    <div class="header-badge">✿ Kelompok 7 · LPK 2026 ✿</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✿ Parameter Sampling")
    st.markdown("---")
    lot_size = st.number_input("Ukuran Lot (Batch)", min_value=2, max_value=999999, value=1000, step=50)
    aql_level = st.selectbox("AQL Level (%)", options=AQL_LEVELS, index=6, format_func=lambda x: f"{x}%")
    inspection_type = st.selectbox("Tipe Inspeksi", ["Normal", "Ketat (Tightened)", "Longgar (Reduced)"])
    st.markdown("---")
    st.markdown("### 🌸 Data Defek")
    n_defects = st.number_input("Jumlah Defek Ditemukan", min_value=0, max_value=9999, value=3)
    st.markdown("---")
    st.markdown("### 🌷 Info Lot")
    product_name = st.text_input("Nama Produk/Lot", value="Sampel Kimia A")
    lot_number   = st.text_input("Nomor Lot", value="LOT-2026-001")
    inspector    = st.text_input("Nama Inspektor", value="Kelompok 7")
    analyze_btn  = st.button("Analisis Sekarang", use_container_width=True)

# ─────────────────────────────────────────────
# CALCULATION
# ─────────────────────────────────────────────
code_letter = get_code_letter(lot_size)
sample_size = SAMPLE_SIZE.get(code_letter, 2)
criteria    = get_aql_criteria(code_letter, aql_level)
ac, re      = criteria if criteria else (0, 1)
defect_rate = get_defect_rate(n_defects, sample_size)
decision_pass = n_defects <= ac

# ─────────────────────────────────────────────
# TAB LAYOUT
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🎀 Hasil Analisis", "🌺Visualisasi", "🌸 Tabel AQL", "🌷 Laporan"])

# ── TAB 1: HASIL ──────────────────────────────
with tab1:
    st.markdown('<div class="section-title">Parameter Lot</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    metrics_row1 = [
        (f"{lot_size:,}", "Ukuran Lot"),
        (code_letter,     "Kode Sampel"),
        (str(sample_size),"Ukuran Sampel"),
        (f"{aql_level}%", "AQL Level"),
    ]
    for col, (val, lbl) in zip([c1,c2,c3,c4], metrics_row1):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Kriteria Penerimaan</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    metrics_row2 = [
        (str(ac),                "Accept Number (Ac)"),
        (str(re),                "Reject Number (Re)"),
        (str(n_defects),         "Defek Ditemukan"),
        (f"{defect_rate:.2f}%",  "Defect Rate"),
    ]
    for col, (val, lbl) in zip([c1,c2,c3,c4], metrics_row2):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Keputusan Sampling</div>', unsafe_allow_html=True)
    if decision_pass:
        st.markdown(f"""
        <div class="result-pass">
            <div class="result-pass-text">🌸 Lot Diterima (Accept) 🌸</div>
            <div class="result-sub">Defek ({n_defects}) ≤ Ac ({ac}) — Lot memenuhi standar AQL {aql_level}%</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-fail">
            <div class="result-fail-text">🥀 Lot Ditolak (Reject) 🥀</div>
            <div class="result-sub">Defek ({n_defects}) ≥ Re ({re}) — Lot tidak memenuhi standar AQL {aql_level}%</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="section-title">Interpretasi</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.info(f"""
**🌸 Tentang Lot Ini**
- **Produk:** {product_name}
- **Nomor Lot:** {lot_number}
- **Inspektor:** {inspector}
- **Tipe Inspeksi:** {inspection_type}
        """)
    with col_b:
        sampling_ratio = (sample_size / lot_size) * 100
        rekomendasi = (
            "🌸 Lot dapat dikirim/digunakan. Lanjutkan proses produksi normal."
            if decision_pass else
            "🥀 Lakukan inspeksi 100% atau kembalikan ke supplier. Tinjau proses produksi."
        )
        st.warning(f"""
**🎀 Rekomendasi Tindakan**

{rekomendasi}

- Rasio sampling: **{sampling_ratio:.1f}%** dari lot
- Confidence level: **~95%** (General Inspection Level II)
        """)
        
# ── TAB 2: VISUALISASI ────────────────────────
with tab2:
    st.markdown('<div class="section-title">Visualisasi Sampling</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">~ analisis keanggunan akurasi data ~</div>', unsafe_allow_html=True)
    st.markdown('<div class="coquette-bow-decor"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

   # 1. GAUGE CHART
    with col1:
        # PETA WARNA DARURAT (Memastikan variabel warna sudah terdefinisi)
        COQUETTE_PINK = "#F7D7E3"
        COQUETTE_SAGE = "#D0E1D4"
        COQUETTE_ROSE = "#D3A1B0"
        COQUETTE_DARK_TEXT = "#654E4E"
        COQUETTE_BORDER = "#EECAD5"
        
        # Penentu keputusan kelolosan lot
        if 'decision_pass' not in locals() and 'decision_pass' not in globals():
            decision_pass = n_defects <= ac

        # Baris yang tadi eror, sekarang dijamin aman
        gauge_color = COQUETTE_SAGE if decision_pass else COQUETTE_PINK
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=n_defects,
            delta={'reference': ac, 'increasing': {'color': COQUETTE_ROSE}, 'decreasing': {'color': COQUETTE_SAGE}},
            title={'text': "Jumlah Defek vs Batas Terima", 'font': {'color': COQUETTE_DARK_TEXT, 'family': FONT_FAMILY, 'size': 14, 'style': 'italic'}},
            gauge={
                'axis': {'range': [0, max(re*2, n_defects*1.5, 5)], 'tickcolor': COQUETTE_ROSE},
                'bar': {'color': gauge_color, 'thickness': 0.3},
                'bgcolor': 'rgba(255,255,255,0.9)',
                'borderwidth': 1.5,
                'bordercolor': COQUETTE_BORDER,
                'steps': [
                    {'range': [0, ac],                            'color': 'rgba(208,225,212,0.4)'}, 
                    {'range': [ac, re],                           'color': 'rgba(252,245,247,0.8)'}, 
                    {'range': [re, max(re*2, n_defects*1.5, 5)],   'color': 'rgba(247,215,227,0.4)'}, 
                ],
                'threshold': {'line': {'color': COQUETTE_ROSE, 'width': 3}, 'thickness': 0.75, 'value': re}
            },
            number={'font': {'color': COQUETTE_DARK_TEXT, 'family': FONT_FAMILY, 'size': 38}}
        ))
        fig_gauge.update_layout(**coquette_layout(height=320))
        st.plotly_chart(fig_gauge, use_container_width=True)

    # 2. DONUT CHART
    with col2:
        good = max(sample_size - n_defects, 0)
        fig_pie = go.Figure(go.Pie(
            labels=['Kondisi Baik', 'Defek ditemukan'],
            values=[good, n_defects],
            hole=0.6,
            marker=dict(
                colors=[COQUETTE_SAGE, COQUETTE_PINK],
                line=dict(color=COQUETTE_BORDER, width=1.5)
            ),
            textfont=dict(family=FONT_FAMILY, size=13, color=COQUETTE_DARK_TEXT),
        ))
        fig_pie.update_layout(
            **coquette_layout(
                height=320,
                title=dict(text='Komposisi Kualitas Sampel', font=dict(family=FONT_FAMILY, color=COQUETTE_DARK_TEXT, size=14, style='italic')),
            )
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # 3. SENSITIVITY BAR CHART
    st.markdown('<div class="section-title">Zona Keputusan</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">~ status batas penerimaan per jumlah defek ~</div>', unsafe_allow_html=True)
    st.markdown('<div class="coquette-bow-decor"></div>', unsafe_allow_html=True)
    
    max_def = max(int(re * 3), 10)
    defect_range = list(range(0, max_def + 1))
    colors_bar   = [COQUETTE_SAGE if d <= ac else COQUETTE_PINK for d in defect_range]
    
    fig_bar = go.Figure(go.Bar(
        x=defect_range,
        y=[1] * len(defect_range),
        marker=dict(color=colors_bar, line=dict(color=COQUETTE_BORDER, width=1)),
        text=['TERIMA' if d <= ac else 'TOLAK' for d in defect_range],
        textposition='inside',
        textfont=dict(family=FONT_FAMILY, size=10, color=COQUETTE_DARK_TEXT),
        hovertemplate="Jumlah Defek: %{x}<br>Status: %{text}<extra></extra>"
    ))
    fig_bar.add_vline(x=ac+0.5, line_color=COQUETTE_ROSE, line_dash='dash', line_width=2,
                     annotation_text=f'Batas Ac={ac}', annotation_font_color=COQUETTE_ROSE)
    fig_bar.update_layout(
        **coquette_layout(
            height=200,
            xaxis=dict(title='Jumlah Defek', gridcolor='rgba(238,202,213,0.3)', tickcolor=COQUETTE_ROSE, color=COQUETTE_DARK_TEXT, dtick=1),
            yaxis=dict(visible=False, showgrid=False)
        )
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # 4. OC CURVE
    st.markdown('<div class="section-title">Kurva Karakteristik Operasi</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">~ probabilitas penerimaan lot produk ~</div>', unsafe_allow_html=True)
    st.markdown('<div class="coquette-bow-decor"></div>', unsafe_allow_html=True)
    
    p_values  = np.linspace(0, 0.3, 200)
    pa_values = stats.binom.cdf(ac, sample_size, p_values) * 100

    fig_oc = go.Figure()
    fig_oc.add_trace(go.Scatter(
        x=p_values*100, y=pa_values,
        mode='lines', name='P(Accept)',
        line=dict(color=COQUETTE_ROSE, width=3),
        fill='tozeroy', fillcolor='rgba(247,215,227,0.2)', # Isian pink transparan lembut
        hovertemplate="Rasio Defek: %{x:.2f}%<br>P(Diterima): %{y:.2f}%<extra></extra>"
    ))
    fig_oc.add_vline(x=aql_level, line_color=COQUETTE_DARK_TEXT, line_dash='dot', line_width=1.5,
                     annotation_text=f'AQL={aql_level}%', annotation_font_color=COQUETTE_DARK_TEXT)
    fig_oc.add_hline(y=95, line_color='rgba(101,78,78,0.4)', line_dash='dot',
                     annotation_text='95% Kriteria Produsen', annotation_font_color=COQUETTE_DARK_TEXT)
    fig_oc.update_layout(
        **coquette_layout(
            height=300,
            xaxis=dict(title='Defect Rate di Pasar (%)', gridcolor='rgba(238,202,213,0.3)', tickcolor=COQUETTE_ROSE, color=COQUETTE_DARK_TEXT),
            yaxis=dict(title='P(Accept) %', gridcolor='rgba(238,202,213,0.3)', tickcolor=COQUETTE_ROSE, color=COQUETTE_DARK_TEXT, range=[0,105])
        )
    )
    st.plotly_chart(fig_oc, use_container_width=True)
    
# ── TAB 3: TABEL AQL ─────────────────────────
with tab3:
    st.markdown('<div class="section-title">Tabel Referensi AQL (ISO 2859-1 — Normal Inspection)</div>', unsafe_allow_html=True)

    rows = []
    for low, high, code in LOT_SIZE_TABLE:
        n   = SAMPLE_SIZE[code]
        row = {
            'Ukuran Lot': f"{low:,} – {high:,}" if high != float('inf') else f"≥ {low:,}",
            'Kode': code,
            'n Sampel': n,
        }
        for aql_v in [0.65, 1.0, 1.5, 2.5, 4.0, 6.5]:
            crit = AQL_TABLE[code].get(aql_v, (0, 1))
            row[f'AQL {aql_v}%'] = f"Ac={crit[0]}  Re={crit[1]}"
        rows.append(row)

    df_table = pd.DataFrame(rows)

    def highlight_current(row):
        if row['Kode'] == code_letter:
            return ['background-color: rgba(224,112,144,0.12); color: #c05070'] * len(row)
        return [''] * len(row)

    st.dataframe(
        df_table.style.apply(highlight_current, axis=1),
        use_container_width=True, height=420
    )
    st.caption(f"🎀 Baris yang di-highlight = kode {code_letter} sesuai lot size {lot_size:,}")

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

# ── TAB 4: LAPORAN ────────────────────────────
with tab4:
    st.markdown('<div class="section-title">Laporan Hasil Sampling</div>', unsafe_allow_html=True)

    from datetime import datetime
    from zoneinfo import ZoneInfo
    from fpdf import FPDF
    import io

    waktu_jakarta = ZoneInfo("Asia/Jakarta")
    now = datetime.now(waktu_jakarta).strftime("%d %B %Y, %H:%M WIB")

    report_text_markdown = f"""
## 🎀 Laporan Hasil Sampling AQL
**Tanggal:** {now}

---

### 🌸 Identifikasi Lot
| Parameter | Nilai |
|---|---|
| Nama Produk | {product_name} |
| Nomor Lot | {lot_number} |
| Inspektor | {inspector} |
| Tipe Inspeksi | {inspection_type} |

### 🌷 Parameter Sampling (ISO 2859-1)
| Parameter | Nilai |
|---|---|
| Ukuran Lot | {lot_size:,} unit |
| Kode Sampel | {code_letter} |
| Ukuran Sampel (n) | {sample_size} unit |
| AQL Level | {aql_level}% |
| Accept Number (Ac) | {ac} |
| Reject Number (Re) | {re} |

### 🎀 Hasil Pemeriksaan
| Parameter | Nilai |
|---|---|
| Jumlah Defek Ditemukan | {n_defects} unit |
| Defect Rate | {defect_rate:.3f}% |
| Keputusan | **{"ACCEPT 🌸" if decision_pass else "REJECT 🥀"}** |

### Dasar Keputusan
{"Lot **DITERIMA** karena jumlah defek ditemukan (" + str(n_defects) + ") tidak melebihi Accept Number (" + str(ac) + ") sesuai standar AQL " + str(aql_level) + "%." if decision_pass else "Lot **DITOLAK** karena jumlah defek ditemukan (" + str(n_defects) + ") mencapai atau melebihi Reject Number (" + str(re) + ") sesuai standar AQL " + str(aql_level) + "%."}

### Rekomendasi Tindakan
{"🌸 Lot dapat diterima dan diteruskan ke proses selanjutnya. Pertahankan standar produksi saat ini." if decision_pass else "🥀 Lot ditolak. Lakukan salah satu:\n1. Inspeksi 100% seluruh lot\n2. Kembalikan ke supplier (jika material dari luar)\n3. Lakukan analisis akar masalah (root cause analysis)\n4. Review dan perbaiki proses produksi"}

---
*Laporan ini dibuat otomatis menggunakan AQL Sampling Analyzer — Kelompok 7 LPK 2026*
*Standar Referensi: ISO 2859-1 (Sampling procedures for inspection by attributes)*
    """
    
    st.markdown(report_text_markdown)

    def buat_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        
        pdf.set_font("Helvetica", style="B", size=16)
        pdf.cell(200, 10, txt="LAPORAN HASIL SAMPLING AQL", ln=True, align='C')
        pdf.set_font("Helvetica", size=10)
        pdf.cell(200, 10, txt=f"Tanggal Cetak: {now}", ln=True, align='C')
        pdf.ln(10)
        
        def tambah_baris(label, nilai):
            pdf.set_font("Helvetica", style="B", size=11)
            pdf.cell(60, 8, txt=f"{label}:", border=0)
            pdf.set_font("Helvetica", size=11)
            pdf.cell(130, 8, txt=str(nilai), border=0, ln=True)

        pdf.set_font("Helvetica", style="B", size=13)
        pdf.cell(200, 8, txt="I. IDENTIFIKASI LOT", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)
        tambah_baris("Nama Produk", product_name)
        tambah_baris("Nomor Lot", lot_number)
        tambah_baris("Inspektor", inspector)
        tambah_baris("Tipe Inspeksi", inspection_type)
        pdf.ln(5)

        pdf.set_font("Helvetica", style="B", size=13)
        pdf.cell(200, 8, txt="II. PARAMETER SAMPLING (ISO 2859-1)", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)
        tambah_baris("Ukuran Lot", f"{lot_size:,} unit")
        tambah_baris("Kode Sampel", code_letter)
        tambah_baris("Ukuran Sampel (n)", f"{sample_size} unit")
        tambah_baris("AQL Level", f"{aql_level}%")
        tambah_baris("Accept Number (Ac)", ac)
        tambah_baris("Reject Number (Re)", re)
        pdf.ln(5)

        pdf.set_font("Helvetica", style="B", size=13)
        pdf.cell(200, 8, txt="III. HASIL PEMERIKSAAN & KEPUTUSAN", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)
        tambah_baris("Jumlah Defek Ditemukan", f"{n_defects} unit")
        tambah_baris("Defect Rate", f"{defect_rate:.3f}%")
        status_keputusan = "ACCEPT" if decision_pass else "REJECT"
        tambah_baris("Keputusan Akhir", status_keputusan)
        pdf.ln(4)

        pdf.set_font("Helvetica", style="B", size=11)
        pdf.cell(200, 6, txt="Dasar Keputusan:", ln=True)
        pdf.set_font("Helvetica", size=11)
        txt_dasar = f"Lot DITERIMA karena jumlah defek ditemukan ({n_defects}) tidak melebihi Accept Number ({ac}) sesuai standar AQL {aql_level}%." if decision_pass else f"Lot DITOLAK karena jumlah defek ditemukan ({n_defects}) mencapai atau melebihi Reject Number ({re}) sesuai standar AQL {aql_level}%."
        pdf.multi_cell(190, 6, txt=txt_dasar)
        pdf.ln(4)

        pdf.set_font("Helvetica", style="B", size=11)
        pdf.cell(200, 6, txt="Rekomendasi Tindakan:", ln=True)
        pdf.set_font("Helvetica", size=11)
        txt_rekomendasi = "Lot dapat diterima dan diteruskan ke proses selanjutnya. Pertahankan standar produksi saat ini." if decision_pass else "Lot ditolak. Lakukan salah satu:\n1. Inspeksi 100% seluruh lot\n2. Kembalikan ke supplier\n3. Lakukan analisis akar masalah (root cause analysis)\n4. Review dan perbaiki proses produksi"
        pdf.multi_cell(190, 6, txt=txt_rekomendasi)
        
        pdf.ln(15)
        pdf.set_font("Helvetica", style="I", size=9)
        pdf.cell(200, 5, txt="Laporan ini dibuat otomatis menggunakan AQL Sampling Analyzer - Kelompok 7 LPK 2026", ln=True, align='C')
        pdf.cell(200, 5, txt="Standar Referensi: ISO 2859-1", ln=True, align='C')
        
        return pdf.output()

    pdf_data = buat_pdf()

    st.download_button(
        label="🎀 Unduh Laporan Resmi (.pdf)",
        data=bytes(pdf_data),
        file_name=f"laporan_aql_{lot_number.replace('-','_')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    st.markdown("---")
    st.markdown("""
<div style="text-align:center; color:#b08090; font-family:'Cormorant Garamond', serif; font-style:italic; letter-spacing:2px; font-size:0.95rem; margin-top:10px;">
    ✿ AQL Sampling Analyzer · Kelompok 7 · LPK 2026 ✿<br>
    <span style="font-size:0.80rem;">Standar: ISO 2859-1 · General Inspection Level II · Single Sampling Normal</span>
</div>
""", unsafe_allow_html=True)
