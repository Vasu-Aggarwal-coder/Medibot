# ─────────────────────────────────────────────
# app.py  —  entry point
#
# Run with:  streamlit run app.py
#
# Responsibilities:
#   1. Configure the Streamlit page
#   2. Initialise session state
#   3. Load shared resources (logo)
#   4. Inject styles
#   5. Delegate every UI section to its module
#   6. Handle the chat input / query dispatch loop
# ─────────────────────────────────────────────

import streamlit as st
import streamlit.components.v1 as components

# ── project modules ──────────────────────────
from config.constants  import LANGUAGES, PLACEHOLDERS, PAGE_CONFIG, LOGO_FILENAME
from utils.image       import get_image_b64
from utils.tts         import mic_button_html
from ui.styles         import inject_styles
from ui.layout         import (
    render_sidebar,
    render_sidebar_toggle,
    render_hero,
    render_welcome_panel,
    render_footer,
)
from ui.chat           import render_chat_history, process_query
from core.rag          import multilingual_rag, retriever


# ─────────────────────────────────────────────
# 1. PAGE CONFIG  (must be the very first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(**PAGE_CONFIG)


# ─────────────────────────────────────────────
# 2. SESSION STATE
# ─────────────────────────────────────────────
if "messages"      not in st.session_state: st.session_state.messages      = []
if "selected_lang" not in st.session_state: st.session_state.selected_lang = "English"
if "suggestion"    not in st.session_state: st.session_state.suggestion    = None


# ─────────────────────────────────────────────
# 3. SHARED RESOURCES  (loaded once at startup)
# ─────────────────────────────────────────────
LOGO_URI = get_image_b64(LOGO_FILENAME)


# ─────────────────────────────────────────────
# 4. STYLES
# ─────────────────────────────────────────────
inject_styles()


# ─────────────────────────────────────────────
# 5. SIDEBAR  (returns the chosen language)
# ─────────────────────────────────────────────
selected_lang = render_sidebar(st.session_state.selected_lang)
st.session_state.selected_lang = selected_lang
lang = LANGUAGES[selected_lang]


# ─────────────────────────────────────────────
# 6. FLOATING SIDEBAR TOGGLE BUTTON
# ─────────────────────────────────────────────
render_sidebar_toggle()


# ─────────────────────────────────────────────
# 7. HERO BANNER
# ─────────────────────────────────────────────
render_hero(LOGO_URI)


# ─────────────────────────────────────────────
# 8. WELCOME PANEL  (only when chat is empty)
# ─────────────────────────────────────────────
if not st.session_state.messages:
    render_welcome_panel(LOGO_URI)


# ─────────────────────────────────────────────
# 9. CHAT HISTORY
# ─────────────────────────────────────────────
render_chat_history(tts_code=lang["tts"])


# ─────────────────────────────────────────────
# 10. MICROPHONE BUTTON
# ─────────────────────────────────────────────
components.html(mic_button_html(lang["tts"]), height=0)


# ─────────────────────────────────────────────
# 11. CHAT INPUT
# ─────────────────────────────────────────────
typed_prompt = st.chat_input(
    PLACEHOLDERS.get(selected_lang, "यहाँ अपना प्रश्न लिखें…")
)


# ─────────────────────────────────────────────
# 12. QUERY DISPATCH
#     Priority: suggestion button click > typed input
# ─────────────────────────────────────────────
final_prompt = st.session_state.suggestion or typed_prompt

# Consume the suggestion so it doesn't fire again on next rerun
if st.session_state.suggestion:
    st.session_state.suggestion = None

if final_prompt:
    process_query(
        prompt=final_prompt,
        lang_code=lang["code"],
        multilingual_rag=multilingual_rag,
        retriever=retriever,
    )


# ─────────────────────────────────────────────
# 13. FOOTER
# ─────────────────────────────────────────────
render_footer()