import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st

from backend.predictor import (
    load_ml_assets,
    make_prediction,
    PredictionError,
)

from data.locations import (
    STATES,
    STATE_DISTRICTS,
    CROPS,
    SEASONS,
)

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="KrushiMitra | AI Crop Yield Prediction",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CUSTOM CSS (DARK GLASSMORPHISM / PREMIUM SAAS)
# ==========================================
def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

        :root {
            --primary: #00D4FF;
            --secondary: #7CF29C;
            --text-main: #E6EDF3;
            --text-muted: #7D8AA3;
            --border-soft: rgba(255,255,255,0.08);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Hide default Streamlit chrome for a clean, branded shell */
        #MainMenu, header, footer { visibility: hidden; }
        div[data-testid="stToolbar"] { visibility: hidden; height: 0; }
        div[data-testid="stDecoration"] { display: none; }

        /* Background */
        .stApp {
            background:
                radial-gradient(circle at 12% 8%, rgba(0,212,255,0.12), transparent 42%),
                radial-gradient(circle at 88% 12%, rgba(124,242,156,0.09), transparent 45%),
                radial-gradient(circle at 50% 105%, rgba(0,212,255,0.08), transparent 55%),
                linear-gradient(180deg, #04060B 0%, #070B14 45%, #05080F 100%);
            color: var(--text-main);
        }

        .block-container {
            padding-top: 2.4rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 10px; height: 10px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(0,212,255,0.35); }
        ::selection { background: rgba(0,212,255,0.35); color: #fff; }

        /* ===================== HERO ===================== */
        .hero-wrap { margin-bottom: 8px; animation: fadeUp 0.7s ease; }
        .brand-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 14px;
            margin-bottom: 26px;
        }
        .brand-left { display: flex; align-items: center; gap: 14px; }
        .logo-mark {
            width: 50px; height: 50px;
            border-radius: 15px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            display: flex; align-items: center; justify-content: center;
            font-size: 26px;
            box-shadow: 0 10px 28px rgba(0,212,255,0.30);
        }
        .brand-name {
            font-family: 'Sora', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: #fff;
            line-height: 1.1;
        }
        .brand-tag {
            font-size: 0.74rem;
            color: var(--text-muted);
            letter-spacing: 0.09em;
            text-transform: uppercase;
            margin-top: 2px;
        }
        .status-badge {
            display: inline-flex; align-items: center; gap: 8px;
            padding: 9px 16px;
            border-radius: 999px;
            background: rgba(124,242,156,0.08);
            border: 1px solid rgba(124,242,156,0.28);
            font-size: 0.8rem; font-weight: 600;
            color: var(--secondary);
            white-space: nowrap;
        }
        .status-dot {
            width: 8px; height: 8px; border-radius: 50%;
            background: var(--secondary);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%   { box-shadow: 0 0 0 0 rgba(124,242,156,0.55); }
            70%  { box-shadow: 0 0 0 9px rgba(124,242,156,0); }
            100% { box-shadow: 0 0 0 0 rgba(124,242,156,0); }
        }
        .hero-title {
            font-family: 'Sora', sans-serif;
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1.15;
            margin: 0 0 10px 0;
            background: linear-gradient(90deg, #ffffff 0%, var(--primary) 55%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
            color: var(--text-muted);
            font-size: 1.02rem;
            font-weight: 400;
            max-width: 620px;
            line-height: 1.55;
            margin-bottom: 8px;
        }

        /* ===================== PANEL / SECTION LABELS ===================== */
        .panel-label {
            display: flex; align-items: center; gap: 9px;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.11em;
            text-transform: uppercase;
            color: var(--text-muted);
            margin: 4px 0 20px 2px;
        }
        .panel-label .dot {
            width: 6px; height: 6px; border-radius: 50%;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
        }

        /* ===================== GLASS PANELS (bordered containers) ===================== */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(255,255,255,0.025);
            border: 1px solid var(--border-soft);
            border-radius: 22px;
            backdrop-filter: blur(22px);
            -webkit-backdrop-filter: blur(22px);
            box-shadow: 0 10px 44px rgba(0,0,0,0.35);
            transition: border-color 0.3s ease, transform 0.3s ease;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color: rgba(255,255,255,0.14);
        }
        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            padding: 8px 6px;
        }

        /* ===================== FORM INPUTS ===================== */
        .stSelectbox label, .stNumberInput label {
            color: #AAB4C5 !important;
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.05em !important;
            text-transform: uppercase;
        }
        div[data-baseweb="select"] > div {
            background-color: rgba(255,255,255,0.035) !important;
            border: 1px solid var(--border-soft) !important;
            border-radius: 12px !important;
            color: var(--text-main) !important;
            min-height: 46px;
            transition: border-color 0.2s ease;
        }
        div[data-baseweb="select"] > div:hover {
            border-color: rgba(0,212,255,0.45) !important;
        }
        ul[data-baseweb="menu"] {
            background-color: #0B0F1A !important;
            border: 1px solid var(--border-soft) !important;
            border-radius: 12px !important;
        }
        li[data-baseweb="menu-item"]:hover {
            background-color: rgba(0,212,255,0.10) !important;
        }
        .stNumberInput input {
            background-color: rgba(255,255,255,0.035) !important;
            border: 1px solid var(--border-soft) !important;
            border-radius: 12px !important;
            color: var(--text-main) !important;
            min-height: 46px;
        }
        .stNumberInput input:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(0,212,255,0.15) !important;
        }
        .stNumberInput button {
            background: rgba(255,255,255,0.04) !important;
            border-color: var(--border-soft) !important;
            color: var(--text-main) !important;
        }

        /* ===================== BUTTON ===================== */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: #04070D;
            font-weight: 800;
            font-size: 1.02rem;
            border: none;
            border-radius: 14px;
            padding: 16px;
            margin-top: 8px;
            letter-spacing: 0.01em;
            box-shadow: 0 12px 32px rgba(0,212,255,0.25);
            transition: transform 0.22s ease, box-shadow 0.22s ease, opacity 0.22s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px) scale(1.008);
            box-shadow: 0 16px 42px rgba(0,212,255,0.40);
            opacity: 0.97;
            color: #04070D;
        }
        .stButton > button:active { transform: translateY(0) scale(0.99); }

        /* ===================== ALERTS / SPINNER ===================== */
        div[data-testid="stAlert"] {
            background: rgba(255,255,255,0.04) !important;
            border: 1px solid var(--border-soft) !important;
            border-radius: 12px !important;
            backdrop-filter: blur(10px);
        }
        .stSpinner > div { color: var(--primary) !important; }

        /* ===================== EMPTY STATE ===================== */
        .empty-state { text-align: center; padding: 34px 18px 14px; animation: fadeUp 0.5s ease; }
        .empty-icon { margin-bottom: 18px; display: flex; justify-content: center; }
        .empty-title {
            font-family: 'Sora', sans-serif;
            font-size: 1.28rem; font-weight: 700;
            color: #EDF2F7; margin-bottom: 10px;
        }
        .empty-desc {
            color: var(--text-muted);
            font-size: 0.92rem; line-height: 1.6;
            max-width: 320px; margin: 0 auto;
        }

        /* ===================== RESULT STATE ===================== */
        .result-wrap { text-align: center; padding: 22px 10px 10px; animation: fadeUp 0.6s ease; }
        .success-pill {
            display: inline-flex; align-items: center; gap: 7px;
            padding: 7px 15px; border-radius: 999px;
            background: rgba(124,242,156,0.10);
            border: 1px solid rgba(124,242,156,0.30);
            color: var(--secondary);
            font-size: 0.76rem; font-weight: 700;
            text-transform: uppercase; letter-spacing: 0.07em;
            margin-bottom: 20px;
        }
        .yield-label {
            color: var(--text-muted);
            font-size: 0.85rem; font-weight: 600;
            text-transform: uppercase; letter-spacing: 0.06em;
            margin-bottom: 2px;
        }
        .yield-value {
            font-family: 'Sora', sans-serif;
            font-size: 4rem; font-weight: 800;
            line-height: 1.05;
            margin: 4px 0 2px 0;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .yield-unit {
            color: var(--text-muted);
            font-size: 0.95rem; font-weight: 600;
            letter-spacing: 0.03em;
            margin-bottom: 20px;
        }
        .confidence-tag {
            display: inline-block;
            padding: 9px 18px; border-radius: 12px;
            background: rgba(0,212,255,0.07);
            border: 1px solid rgba(0,212,255,0.20);
            color: #9FD8F5;
            font-size: 0.78rem; font-weight: 600;
        }

        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(14px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        /* ===================== METRIC CARDS ===================== */
        .metric-card {
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--border-soft);
            border-radius: 16px;
            padding: 20px 14px;
            text-align: center;
            transition: transform 0.25s ease, border-color 0.25s ease;
            height: 100%;
        }
        .metric-card:hover {
            transform: translateY(-4px);
            border-color: rgba(0,212,255,0.30);
        }
        .metric-icon { font-size: 1.35rem; margin-bottom: 10px; }
        .metric-val {
            font-family: 'Sora', sans-serif;
            font-size: 1.45rem; font-weight: 800;
            color: #fff;
        }
        .metric-val.accent {
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .metric-lbl {
            color: var(--text-muted);
            font-size: 0.70rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-top: 8px;
        }
        

        /* ===================== FOOTER ===================== */
        .app-footer {
            text-align: center;
            padding-top: 34px;
            padding-bottom: 6px;
            color: #5C6780;
            font-size: 0.82rem;
            border-top: 1px solid var(--border-soft);
            margin-top: 38px;
            line-height: 1.8;
        }
        .app-footer b { color: #AAB4C5; }

        /* ===================== RESPONSIVE ===================== */
        @media (max-width: 768px) {
            .hero-title { font-size: 1.9rem; }
            .yield-value { font-size: 2.9rem; }
            .metric-card { padding: 14px 8px; }
            .block-container { padding-top: 1.4rem; }
        }
        /* Animation for the result to pop in */
        .result-fade-in {
            animation: fadeIn 0.8s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.98); }
            to { opacity: 1; transform: scale(1); }
        }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# UI COMPONENTS
# ==========================================
def render_hero():
    st.markdown("""
        <div class="hero-wrap">
            <div class="brand-row">
                <div class="brand-left">
                    <div class="logo-mark">🌱</div>
                    <div>
                        <div class="brand-name">KrushiMitra</div>
                        <div class="brand-tag">AI Crop Intelligence Platform</div>
                    </div>
                </div>
                <div class="status-badge">
                    <span class="status-dot"></span>AI Engine Active
                </div>
            </div>
            <h1 class="hero-title">AI-Powered Crop Yield Prediction</h1>
            <p class="hero-subtitle">
                Forecast crop yield in seconds using a Random Forest Regressor trained on
                large-scale historical agricultural data across India.
            </p>
        </div>
    """, unsafe_allow_html=True)


def render_empty_state():
    st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">
                <svg width="76" height="76" viewBox="0 0 76 76" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="iconGrad" x1="0" y1="0" x2="76" y2="76" gradientUnits="userSpaceOnUse">
                            <stop stop-color="#00D4FF"/>
                            <stop offset="1" stop-color="#7CF29C"/>
                        </linearGradient>
                    </defs>
                    <circle cx="38" cy="38" r="36" stroke="url(#iconGrad)" stroke-width="1.6" stroke-opacity="0.35"/>
                    <circle cx="38" cy="38" r="25" fill="url(#iconGrad)" fill-opacity="0.08"/>
                    <path d="M38 50V29" stroke="url(#iconGrad)" stroke-width="3" stroke-linecap="round"/>
                    <path d="M38 29C38 29 27 29 25 18C25 18 38 16 38 29Z" fill="url(#iconGrad)" fill-opacity="0.92"/>
                    <path d="M38 33C38 33 49 33 51 22C51 22 38 20 38 33Z" fill="url(#iconGrad)" fill-opacity="0.92"/>
                </svg>
            </div>
            <div class="empty-title">Ready for Prediction</div>
            <p class="empty-desc">
                Configure the crop parameters on the left and click
                <b>Predict Crop Yield</b> to generate an AI-powered forecast.
            </p>
        </div>
    """, unsafe_allow_html=True)


def render_result(predicted_yield):
    st.markdown(f"""
        <div class="result-wrap">
            <div class="success-pill">✅ Prediction Successful</div>
            <div class="yield-label">Estimated Crop Yield</div>
            <div class="yield-value">{predicted_yield:.2f}</div>
            <div class="yield-unit">Tons / Hectare</div>
            <div class="confidence-tag">🤖 Model R² Confidence Score: 92.78%</div>
        </div>
    """, unsafe_allow_html=True)


def render_analytics():
    st.markdown('<div class="panel-label"><span class="dot"></span>Model Performance</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#7D8AA3;font-size:0.88rem;margin-top:-10px;margin-bottom:22px;'>"
        "Random Forest Regressor evaluated on 345,308 historical records.</p>",
        unsafe_allow_html=True
    )

    metrics = [
        ("📈", "R² Score", "92.78%", True),
        ("📉", "Mean Absolute Error", "13.676", False),
        ("📊", "Root Mean Sq. Error", "248.663", False),
        ("🗂️", "Training Samples", "276,246", False),
        ("🧪", "Testing Samples", "69,062", False),
    ]

    cols = st.columns(5, gap="medium")
    for col, (icon, label, value, accent) in zip(cols, metrics):
        with col:
            accent_class = "accent" if accent else ""
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">{icon}</div>
                    <div class="metric-val {accent_class}">{value}</div>
                    <div class="metric-lbl">{label}</div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
                <div >
                </div>
            """, unsafe_allow_html=True)


def render_footer():
    st.markdown("""
        <div class="app-footer">
            <b>🌱 KrushiMitra</b> — AI Crop Yield Prediction<br>
            Built with Python • Scikit-learn • Streamlit
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# MAIN APPLICATION LOGIC
# ==========================================
def main():
    inject_custom_css()

    # Load Models
    model, preprocessor = load_ml_assets()
    if model is None or preprocessor is None:
        return

    render_hero()

    # Layout: Two main columns
    left_col, right_col = st.columns([1.2, 1], gap="large")

    with left_col:
        with st.container(border=True):
            st.markdown('<div class="panel-label"><span class="dot"></span>Crop Parameter Input</div>', unsafe_allow_html=True)

            # Form inputs
            col_a, col_b = st.columns(2)
            with col_a:
                state = st.selectbox(
                    "State",
                    STATES
                )

                crop = st.selectbox(
                    "Crop",
                    CROPS
                )

                crop_year = st.number_input(
                    "Crop Year",
                    min_value=1990,
                    max_value=2030,
                    value=2024,
                    step=1
                )
            with col_b:

                district = st.selectbox(
                    "District",
                    STATE_DISTRICTS.get(state, [])
                )

                season = st.selectbox(
                    "Season",
                    SEASONS
                )

                area = st.number_input(
                    "Area (in hectares)",
                    min_value=0.1,
                    value=100.0,
                    step=10.0
                )

            # Trigger Prediction
            predict_btn = st.button("🔮 Predict Crop Yield", use_container_width=True)

    with right_col:
        with st.container(border=True):
            st.markdown('<div class="panel-label"><span class="dot"></span>Prediction Result</div>', unsafe_allow_html=True)

            if predict_btn:
                with st.spinner("AI is analyzing parameters..."):

                    input_data = {
                        "State": state,
                        "District": district,
                        "Crop": crop,
                        "Season": season,
                        "Crop_Year": crop_year,
                        "Area": area,
                    }

                    try:
                        predicted_yield = make_prediction(
                            model,
                            preprocessor,
                            input_data
                        )

                    except PredictionError as e:
                        st.error(str(e))
                        st.stop()

                    except Exception as e:
                        st.error(f"Unexpected Error: {e}")
                        st.stop()

                render_result(predicted_yield)
            else:
                render_empty_state()

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # ===========================
    # Analytics (Always Visible, full width)
    # ===========================
    with st.container(border=True):
        render_analytics()

    render_footer()


if __name__ == "__main__":
    main()