# ─────────────────────────────────────────────
# ui/layout.py
# Renders the hero banner, welcome panel, sidebar and footer.
# Each function receives only the data it needs.
# ─────────────────────────────────────────────

import streamlit as st
import streamlit.components.v1 as components

from config.constants import LANGUAGES, TOPICS, SUGGESTIONS


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

def render_sidebar(current_lang: str) -> str:
    """
    Render the sidebar with language selector and clear button.

    Args:
        current_lang: Currently selected language key, e.g. "English".

    Returns:
        The newly selected language key (may be unchanged).
    """
    with st.sidebar:
        st.markdown("""
<div style="padding: 18px 8px 12px; text-align: center;">
    <h1 style="font-family:'Libre Baskerville',serif; color:#ffffff; font-size:1.3rem;
               font-weight:700; margin:0; line-height:1.3;">
        Agriculture Chatbot<br>GB Pant University, Pantnagar
    </h1>
    <div style="font-family:'Tiro Devanagari Hindi',serif; color:#f0c040;
                font-size:0.95rem; margin-top:8px;">
        कृषि एवं प्रौद्योगिकी AI सहायक  Ask Anything About Farming
    </div>
    <div style="color:rgba(255,255,255,0.85); font-size:0.75rem; font-style:italic;
                margin-top:10px; border-top:1px solid rgba(255,255,255,0.2);
                padding-top:8px; line-height:1.5;">
        "Your AI-powered assistant for crop management, irrigation, pest control,
        and agricultural best practices"
    </div>
</div>
""", unsafe_allow_html=True)

        st.divider()

        selected_lang = st.radio(
            "🌐 Language / भाषा",
            options=list(LANGUAGES.keys()),
            index=list(LANGUAGES.keys()).index(current_lang),
            format_func=lambda x: f"{LANGUAGES[x]['flag']}  {x}",
            horizontal=True,
        )

        st.divider()

        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages   = []
            st.session_state.suggestion = None
            st.rerun()

        st.markdown("""
<div style='margin-top:16px; padding:12px; background:rgba(255,255,255,0.1);
            border-radius:8px; font-size:0.75rem; color:rgba(255,255,255,0.8); line-height:1.6;'>
    🎤 Voice input (Chrome/Edge)<br>
    📄 Source-backed answers<br>
    🌐 English &amp; हिंदी support<br>
    🌾 Agriculture &amp; Technology
</div>
""", unsafe_allow_html=True)

    return selected_lang


# ─────────────────────────────────────────────
# FLOATING SIDEBAR TOGGLE
# ─────────────────────────────────────────────

def render_sidebar_toggle() -> None:
    """Inject the custom floating ◄/► sidebar toggle button."""
    components.html("""
<script>
(function() {
    var resizeObs = null;

    function setup() {
        var par = window.parent;
        if (!par || !par.document || !par.document.body) return false;

        var sidebar = par.document.querySelector('[data-testid="stSidebar"]');
        if (!sidebar) return false;

        var old = par.document.getElementById('custom-sidebar-btn');
        if (old) old.remove();
        if (resizeObs) { resizeObs.disconnect(); resizeObs = null; }

        var btn = par.document.createElement('button');
        btn.id    = 'custom-sidebar-btn';
        btn.title = 'Toggle Sidebar';

        btn.style.cssText = [
            'position:fixed','top:50%','left:0px',
            'transform:translateY(-50%)','z-index:999999',
            'background:#7a0012','color:white','border:none',
            'border-top-right-radius:8px','border-bottom-right-radius:8px',
            'border-top-left-radius:0','border-bottom-left-radius:0',
            'width:26px','height:52px','cursor:pointer',
            'font-size:1.0rem','box-shadow:3px 0 10px rgba(0,0,0,0.35)',
            'display:flex','align-items:center','justify-content:center',
            'padding:0','line-height:1','transition:background 0.15s'
        ].join(';');

        function getSidebarWidth() { return sidebar.getBoundingClientRect().width; }

        function refreshIcon(w) { btn.innerHTML = w > 50 ? '\\u25C4' : '\\u25BA'; }

        btn.addEventListener('mouseenter', function() { this.style.background = '#9b0020'; });
        btn.addEventListener('mouseleave', function() { this.style.background = '#7a0012'; });

        btn.addEventListener('click', function() {
            var native =
                par.document.querySelector('[data-testid="collapsedControl"] button') ||
                par.document.querySelector('[data-testid="stSidebarCollapseButton"] button');
            if (native) { native.click(); return; }
            var w = getSidebarWidth();
            if (w < 10) {
                sidebar.style.removeProperty('width');
                sidebar.style.removeProperty('min-width');
                sidebar.style.removeProperty('overflow');
            } else {
                sidebar.style.width = '0px';
                sidebar.style.minWidth = '0px';
                sidebar.style.overflow = 'hidden';
            }
        });

        par.document.body.appendChild(btn);

        var lastW = -1;
        (function rafLoop() {
            var w = getSidebarWidth();
            if (w !== lastW) { lastW = w; btn.style.left = w + 'px'; refreshIcon(w); }
            par.requestAnimationFrame(rafLoop);
        })();

        refreshIcon(getSidebarWidth());
        return true;
    }

    var tries = 0;
    var timer = setInterval(function() {
        if (setup()) { clearInterval(timer); }
        if (++tries > 60) clearInterval(timer);
    }, 150);
})();
</script>
""", height=0)


# ─────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────

def render_hero(logo_uri: str) -> None:
    """
    Render the top hero banner with university logo and title.

    Args:
        logo_uri: Base64 data URI for the logo image.
    """
    st.markdown(f"""
<div class="agri-hero">
    <div class="hero-logo-row">
        <img src="{logo_uri}"
             style="height:200px; width:auto; border-radius:8px;
                    filter:drop-shadow(0 2px 6px rgba(0,0,0,0.3));" />
        <div class="hero-title-block">
            <h1>Agriculture Chatbot<br>GB Pant University, Pantnagar</h1>
            <div class="subtitle-hindi">
                कृषि एवं प्रौद्योगिकी AI सहायक — Ask Anything About Farming
            </div>
        </div>
    </div>
    <div class="hero-tagline">
        "Your AI-powered assistant for crop management, irrigation,
        pest control, and agricultural best practices"
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# WELCOME PANEL
# ─────────────────────────────────────────────

def render_welcome_panel(logo_uri: str) -> None:
    """
    Render the welcome panel with topic grid and suggestion buttons.
    Sets st.session_state.suggestion when a button is clicked.

    Args:
        logo_uri: Base64 data URI for the logo image.
    """
    topic_items_html = "".join(
        f'<div class="topic-item"><span class="icon">{icon}</span><span>{topic}</span></div>'
        for icon, topic in TOPICS
    )

    st.markdown(f"""
<div class="welcome-panel">
    <div class="welcome-content">
        <h2>🙏 आपका स्वागत है — Welcome!</h2>
        <div class="welcome-subtitle">
            Agriculture Chatbot — GB Pant University of Agriculture &amp; Technology
        </div>
        <div class="welcome-desc">
            नमस्ते! I am the AI Agriculture Assistant for GB Pant University, Pantnagar.
            Ask me anything about crops, irrigation, pest control, soil health,
            or farming best practices:
        </div>
        <div class="topic-grid">{topic_items_html}</div>
    </div>
    <div class="inspiration-card">
        <div class="insp-label">Our University</div>
        <img src="{logo_uri}"
             style="height:150px; width:auto; border-radius:8px;
                    filter:drop-shadow(0 2px 6px rgba(0,0,0,0.3));" />
        <div class="insp-name">G. B. Pant University of Agriculture and Technology</div>
        <div class="insp-title">
            Pantnagar University is the first agricultural university established in
            Independent India.<br>
            <strong style="color:#7a0012;">
                It was inaugurated by the first Prime Minister of India Jawahar Lal Nehru
                on 17 November 1960 as the Uttar Pradesh Agricultural University in Pantnagar.
            </strong>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    st.write("")
    st.markdown("**Try a suggestion or type your question below:**")

    col1, col2 = st.columns([1, 1])
    for i, sug in enumerate(SUGGESTIONS):
        with (col1 if i % 2 == 0 else col2):
            if st.button(sug, key=f"sug_{i}", use_container_width=True):
                st.session_state.suggestion = sug
                st.rerun()

    st.write("")


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────

def render_footer() -> None:
    """Render the fixed bottom footer bar."""
    st.markdown("""
<div class="agri-footer">
    Agriculture Chatbot · GB Pant University of Agriculture &amp; Technology, Pantnagar ·
    Content is based on academic and research resources of the university.
</div>
""", unsafe_allow_html=True)