# ─────────────────────────────────────────────
# utils/tts.py
# Browser-side Text-to-Speech and Microphone helpers.
# Each function returns an HTML/JS snippet to be injected
# via st.components.v1.html(..., height=0).
# ─────────────────────────────────────────────


def tts_speak(text: str, tts_code: str) -> str:
    """
    Return an HTML snippet that triggers the Web Speech API
    to read `text` aloud in the given BCP-47 language code.

    Args:
        text:     The string to speak.
        tts_code: BCP-47 tag, e.g. "en-IN" or "hi-IN".

    Returns:
        HTML string with an embedded <script> block.
    """
    lang_root = tts_code.split("-")[0]

    # Escape characters that would break a JS string literal
    safe_text = (
        text
        .replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace('"', '\\"')
        .replace("\n", " ")
        .replace("\r", "")
        .replace("`", "")
    )

    return f"""
<script>
(function() {{
    var ss   = window.speechSynthesis;
    var txt  = '{safe_text}';
    var lng  = '{tts_code}';
    var root = '{lang_root}';
    ss.cancel();

    function bestVoice() {{
        var voices = ss.getVoices();
        return voices.find(function(v) {{ return v.lang === lng; }})
            || voices.find(function(v) {{ return v.lang.startsWith(root); }})
            || null;
    }}

    function doSpeak() {{
        var u   = new SpeechSynthesisUtterance(txt);
        u.lang  = lng;
        u.rate  = 0.92;
        var v   = bestVoice();
        if (v) u.voice = v;
        ss.speak(u);
    }}

    if (ss.getVoices().length > 0) {{
        doSpeak();
    }} else {{
        ss.addEventListener('voiceschanged', function handler() {{
            ss.removeEventListener('voiceschanged', handler);
            doSpeak();
        }});
        setTimeout(function() {{ if (!ss.speaking) doSpeak(); }}, 500);
    }}
}})();
</script>"""


def tts_stop() -> str:
    """
    Return an HTML snippet that cancels any ongoing speech synthesis.

    Returns:
        HTML string with an embedded <script> block.
    """
    return "<script>window.speechSynthesis.cancel();</script>"


def mic_button_html(mic_lang: str) -> str:
    """
    Return an HTML/JS snippet that injects a floating microphone button
    next to Streamlit's chat input.  Clicking it starts the Web Speech
    Recognition API and pastes the transcript into the textarea.

    Args:
        mic_lang: BCP-47 tag used for speech recognition, e.g. "en-IN".

    Returns:
        HTML string with an embedded <script> block.
    """
    return f"""
<script>
(function() {{
    var micLang    = '{mic_lang}';
    var isListening = false;

    function injectMic() {{
        var par = window.parent;
        if (!par || !par.document) return false;

        var ta = par.document.querySelector('[data-testid="stChatInput"] textarea');
        if (!ta) return false;

        if (par.document.getElementById('custom-mic-btn')) return true;

        var mic = par.document.createElement('button');
        mic.id    = 'custom-mic-btn';
        mic.title = 'Click to speak';
        mic.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg"><path d="M12 1a4 4 0 0 1 4 4v6a4 4 0 0 1-8 0V5a4 4 0 0 1 4-4zm-1 17.93V21H9v2h6v-2h-2v-2.07A8 8 0 0 0 20 11h-2a6 6 0 0 1-12 0H4a8 8 0 0 0 7 7.93z"/></svg>';

        mic.style.cssText = [
            'position:fixed',
            'z-index:9999',
            'background:#7a0012',
            'color:white',
            'border:none',
            'border-radius:50%',
            'width:38px',
            'height:38px',
            'min-width:38px',
            'cursor:pointer',
            'display:flex',
            'align-items:center',
            'justify-content:center',
            'padding:0',
            'box-shadow:0 2px 8px rgba(122,0,18,0.35)',
            'transition:background 0.15s, transform 0.15s'
        ].join(';');

        mic.addEventListener('mouseenter', function() {{
            if (!isListening) this.style.background = '#9b0020';
        }});
        mic.addEventListener('mouseleave', function() {{
            if (!isListening) this.style.background = '#7a0012';
        }});

        mic.addEventListener('click', function() {{
            var SR = par.SpeechRecognition || par.webkitSpeechRecognition;
            if (!SR) {{ alert('Speech recognition needs Chrome or Edge.'); return; }}
            if (isListening) return;

            var rec = new SR();
            rec.lang = micLang;
            rec.interimResults = false;

            isListening = true;
            mic.style.background = '#cc0020';
            mic.style.transform  = 'scale(1.15)';

            rec.onresult = function(e) {{
                var text = e.results[0][0].transcript;
                var textarea = par.document.querySelector('[data-testid="stChatInput"] textarea');
                if (textarea) {{
                    var setter = Object.getOwnPropertyDescriptor(par.HTMLTextAreaElement.prototype, 'value').set;
                    setter.call(textarea, text);
                    textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    textarea.focus();
                }}
            }};

            rec.onend = function() {{
                isListening = false;
                mic.style.background = '#7a0012';
                mic.style.transform  = 'scale(1)';
            }};

            rec.onerror = function(e) {{
                isListening = false;
                mic.style.background = '#7a0012';
                mic.style.transform  = 'scale(1)';
                if (e.error !== 'no-speech') alert('Mic error: ' + e.error);
            }};

            rec.start();
        }});

        par.document.body.appendChild(mic);

        // Keep mic button aligned with chat textarea
        (function loop() {{
            var r = ta.getBoundingClientRect();
            mic.style.left = (r.left - 46) + 'px';
            mic.style.top  = (r.top + r.height / 2) + 'px';
            par.requestAnimationFrame(loop);
        }})();

        return true;
    }}

    var tries = 0;
    var t = setInterval(function() {{
        if (injectMic()) {{ clearInterval(t); }}
        if (++tries > 80) clearInterval(t);
    }}, 150);
}})();
</script>"""