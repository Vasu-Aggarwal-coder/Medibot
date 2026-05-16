# ─────────────────────────────────────────────
# ui/styles.py
# Injects all custom CSS into the Streamlit page.
# Call inject_styles() once at the top of app.py.
# ─────────────────────────────────────────────

import streamlit as st


def inject_styles() -> None:
    """Inject the full custom CSS stylesheet into the Streamlit page."""
    st.markdown(_CSS, unsafe_allow_html=True)


_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Tiro+Devanagari+Hindi&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Lato', sans-serif;
}

/* ── Main background ── */
.stApp {
    background-color: #f5f0e8;
    background-image:
        radial-gradient(circle at 20% 80%, rgba(139,0,0,0.04) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(184,134,11,0.04) 0%, transparent 50%);
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer { visibility: hidden; }
header { visibility: hidden; height: 0 !important; }

/* ── Remove extra top padding so hero banner starts at top ── */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    max-width: 100% !important;
}

/* ── Hide the native Streamlit sidebar toggle completely ── */
[data-testid="collapsedControl"] {
    display: none !important;
}

/* ── Our custom floating sidebar open button ── */
#custom-sidebar-btn {
    position: fixed;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    z-index: 999999;
    background: #7a0012;
    color: white;
    border: none;
    border-radius: 0 8px 8px 0;
    width: 28px;
    height: 56px;
    cursor: pointer;
    font-size: 1.1rem;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.35);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s, width 0.2s;
}
#custom-sidebar-btn:hover {
    background: #9b0020;
    width: 34px;
}

[data-testid="stSidebarCollapseButton"] button {
    color: white !important;
}
[data-testid="stSidebarCollapseButton"] svg {
    fill: white !important;
    color: white !important;
}

/* ── HERO BANNER ── */
.agri-hero {
    background: linear-gradient(135deg, #7a0012 0%, #9b0020 40%, #6d0010 100%);
    border-radius: 0 0 12px 12px;
    padding: 28px 36px 22px;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 0;
    box-shadow: 0 4px 20px rgba(122,0,18,0.35);
}

.agri-hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        repeating-linear-gradient(
            45deg,
            transparent,
            transparent 18px,
            rgba(255,255,255,0.02) 18px,
            rgba(255,255,255,0.02) 19px
        );
}

.hero-logo-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    margin-bottom: 10px;
}

.hero-title-block h1 {
    font-family: 'Libre Baskerville', serif;
    color: #ffffff;
    font-size: 2.0rem;
    font-weight: 700;
    margin: 0;
    line-height: 1.2;
    letter-spacing: 0.5px;
}

.hero-title-block .subtitle-hindi {
    font-family: 'Tiro Devanagari Hindi', serif;
    color: #f0c040;
    font-size: 1.1rem;
    margin-top: 6px;
    font-weight: 400;
}

.hero-tagline {
    color: rgba(255,255,255,0.88);
    font-size: 0.82rem;
    font-style: italic;
    margin-top: 12px;
    line-height: 1.5;
    border-top: 1px solid rgba(255,255,255,0.2);
    padding-top: 10px;
}

/* ── WELCOME PANEL ── */
.welcome-panel {
    background: #fff;
    border: 1px solid #e0d8cc;
    border-radius: 10px;
    padding: 26px 30px;
    margin: 18px 0 0;
    display: flex;
    gap: 24px;
    align-items: flex-start;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
}

.welcome-content { flex: 1; }

.welcome-content h2 {
    font-family: 'Tiro Devanagari Hindi', serif;
    color: #7a0012;
    font-size: 1.35rem;
    margin: 0 0 6px;
}

.welcome-content .welcome-subtitle {
    font-family: 'Libre Baskerville', serif;
    font-weight: 700;
    color: #2c1a0e;
    font-size: 0.93rem;
    margin-bottom: 4px;
}

.welcome-content .welcome-desc {
    color: #444;
    font-size: 0.85rem;
    line-height: 1.6;
    margin-bottom: 14px;
}

/* ── TOPIC GRID ── */
.topic-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px 18px;
    margin-top: 8px;
}

.topic-item {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #2c1a0e;
    font-size: 0.84rem;
    padding: 3px 0;
    border-bottom: 1px solid #f0ebe0;
}

.topic-item .icon { font-size: 1.0rem; }

/* ── INSPIRATION CARD ── */
.inspiration-card {
    width: 200px;
    min-width: 180px;
    text-align: center;
    flex-shrink: 0;
}

.inspiration-card .insp-label {
    font-family: 'Libre Baskerville', serif;
    font-weight: 700;
    color: #7a0012;
    font-size: 0.9rem;
    margin-bottom: 8px;
}

.inspiration-card .insp-name {
    font-family: 'Libre Baskerville', serif;
    font-weight: 700;
    color: #7a0012;
    font-size: 0.9rem;
    margin-top: 10px;
    margin-bottom: 2px;
}

.inspiration-card .insp-title {
    color: #555;
    font-size: 0.72rem;
    line-height: 1.5;
}

/* ── CHAT MESSAGES ── */
[data-testid="stChatMessage"] {
    border-radius: 10px !important;
    background: #fff !important;
    border: 1px solid #e8e0d0 !important;
    margin-bottom: 10px !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06) !important;
}

/* ── CHAT INPUT BAR ── */
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInputContainer"],
[data-testid="stChatInputContainer"] > div,
[data-testid="stBottom"],
[data-testid="stBottom"] > div {
    background: #f5f0e8 !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

[data-testid="stChatInput"] {
    z-index: 200 !important;
    padding: 6px 12px !important;
    margin: 0 !important;
    bottom: 20px !important;
}

[data-testid="stChatInputContainer"] {
    padding: 0 !important;
    gap: 4px !important;
    align-items: center !important;
}

[data-testid="stChatInputSubmitButton"] button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 4px !important;
}
[data-testid="stChatInputSubmitButton"] svg {
    fill: #7a0012 !important;
}

[data-testid="stChatInput"] textarea {
    border: 1.5px solid #c8b4a0 !important;
    border-radius: 28px !important;
    background: #ffffff !important;
    font-family: 'Tiro Devanagari Hindi', serif !important;
    font-size: 0.93rem !important;
    padding: 10px 16px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    transition: border-color 0.2s !important;
    resize: none !important;
    line-height: 1.4 !important;
    min-height: 42px !important;
    max-height: 120px !important;
    overflow-y: auto !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: #7a0012 !important;
    box-shadow: 0 0 0 2px rgba(122,0,18,0.10) !important;
    outline: none !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #bbb !important;
    font-style: italic !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #7a0012 0%, #5a000d 100%) !important;
}

[data-testid="stSidebar"] * {
    color: rgba(255,255,255,0.9) !important;
}

[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.15) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    color: white !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.25) !important;
}

[data-testid="stSidebar"] .stRadio label {
    color: rgba(255,255,255,0.9) !important;
}

/* ── SUGGESTION BUTTONS ── */
div[data-testid="column"] .stButton > button {
    background: #fff !important;
    border: 1.5px solid #c8a06a !important;
    color: #5a1a00 !important;
    border-radius: 8px !important;
    font-size: 0.84rem !important;
    padding: 14px 18px !important;
    text-align: left !important;
    white-space: normal !important;
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
    word-break: break-word !important;
    height: auto !important;
    min-height: 60px !important;
    max-height: none !important;
    overflow: visible !important;
    line-height: 1.5 !important;
    display: block !important;
    width: 100% !important;
    transition: all 0.2s !important;
    box-shadow: 0 1px 4px rgba(122,0,18,0.1) !important;
}

div[data-testid="column"] .stButton > button p,
div[data-testid="column"] .stButton > button span {
    white-space: normal !important;
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
    word-break: break-word !important;
    margin: 0 !important;
    display: block !important;
    width: 100% !important;
}

div[data-testid="column"] .stButton {
    height: auto !important;
    display: block !important;
}

div[data-testid="column"] .stButton > button:hover {
    background: #fbf3e8 !important;
    border-color: #7a0012 !important;
    color: #7a0012 !important;
    box-shadow: 0 3px 10px rgba(122,0,18,0.18) !important;
}

/* ── READ/STOP BUTTONS ── */
.read-btn button {
    background: transparent !important;
    border: 1px solid #c0a080 !important;
    color: #7a0012 !important;
    border-radius: 20px !important;
    font-size: 0.78rem !important;
    padding: 4px 12px !important;
}

/* ── FOOTER ── */
.agri-footer {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 250 !important;
    text-align: center;
    color: #999;
    font-size: 0.68rem;
    padding: 0 8px;
    background: #f5f0e8 !important;
    height: 20px;
    line-height: 20px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.main .block-container {
    padding-bottom: 80px !important;
}

/* ── SPINNER ── */
.stSpinner > div { border-top-color: #7a0012 !important; }

/* ── DIVIDER ── */
hr { border-color: #e0d4c0 !important; }

/* ── CAPTION ── */
.stCaption { color: #888 !important; font-size: 0.78rem !important; }
</style>
"""