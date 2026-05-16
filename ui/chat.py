# # ─────────────────────────────────────────────
# # ui/chat.py
# # Renders chat message history and handles new messages.
# # ─────────────────────────────────────────────
# # ui/chat.py

# import os
# import streamlit as st
# import streamlit.components.v1 as components

# from utils.tts import tts_speak, tts_stop
# from core.rag  import translate_with_llm

# HINDI_ERROR = "माफ़ कीजिए, कुछ तकनीकी समस्या आई। कृपया दोबारा प्रयास करें।"


# def render_chat_history(tts_code: str) -> None:
#     """Render all messages. Assistant messages get ▶ Read / ⏹ Stop buttons."""
#     if st.session_state.messages:
#         st.caption("─── Beginning of conversation ───")

#     for i, msg in enumerate(st.session_state.messages):
#         if msg["role"] == "user":
#             with st.chat_message("user"):
#                 st.write(msg["content"])
#         else:
#             with st.chat_message("assistant", avatar="🌾"):
#                 st.write(msg["content"])

#                 if msg.get("sources"):
#                     chips = "   ".join(
#                         f"📄 `{s['source']}` p.{s['page']}" for s in msg["sources"]
#                     )
#                     st.caption(chips)

#                 btn_col1, btn_col2, _ = st.columns([1, 1, 6])
#                 with btn_col1:
#                     if st.button("▶ Read", key=f"read_{i}"):
#                         components.html(tts_speak(msg["content"], tts_code), height=0)
#                 with btn_col2:
#                     if st.button("⏹ Stop", key=f"stop_{i}"):
#                         components.html(tts_stop(), height=0)


# def process_query(prompt: str, lang_code: str, multilingual_rag, retriever) -> None:
#     """
#     Full pipeline:
#       1. RAG runs in English  (multilingual_rag handles Hindi input internally)
#       2. If UI language is Hindi → translate English answer via LLM
#       3. Append messages and rerun
#     """
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     with st.spinner("Thinking… / सोच रहा हूँ…"):
#         try:
#             # Step 1 — RAG (always returns English answer)
#             answer, query_en = multilingual_rag(prompt)
#             #print(f"RAG returned answer: {answer}\n(Original query: {query_en})")
#             # Step 2 — Translate to Hindi if UI is in Hindi mode
#             if lang_code == "hi":
#                 answer = translate_with_llm(answer, target_lang="hi")

#             # Step 3 — Source documents
#             docs = retriever.invoke(query_en)
#             sources = [
#                 {
#                     "source": os.path.basename(doc.metadata.get("source", "Unknown")),
#                     "page":   doc.metadata.get("page", "?"),
#                 }
#                 for doc in docs
#             ]

#             st.session_state.messages.append({
#                 "role":    "assistant",
#                 "content": answer,
#                 "sources": sources,
#             })

#         except Exception as e:
#             st.session_state.messages.append({
#                 "role":    "assistant",
#                 "content": HINDI_ERROR if lang_code == "hi" else f"⚠️ Error: {str(e)}",
#                 "sources": [],
#             })

#     st.rerun()












import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from utils.tts import tts_speak, tts_stop
from core.rag import translate_with_llm

HINDI_ERROR = "माफ़ कीजिए, कुछ तकनीकी समस्या आई। कृपया दोबारा प्रयास करें."


# ─────────────────────────────────────────────
# LOAD CSV (URL DATABASE)
# ─────────────────────────────────────────────
CSV_PATH = "download_log.csv"

try:
    url_df = pd.read_csv(CSV_PATH)
except Exception as e:
    print("CSV load failed:", e)
    url_df = None


def get_url(filename):
    """Map filename → URL from CSV"""
    if url_df is None:
        return None

    row = url_df[url_df["filename"] == filename]

    if row.empty:
        return None

    return row.iloc[0]["url"]


# ─────────────────────────────────────────────
# CHAT HISTORY
# ─────────────────────────────────────────────
def render_chat_history(tts_code: str):

    if st.session_state.messages:
        st.caption("─── Beginning of conversation ───")

    for i, msg in enumerate(st.session_state.messages):

        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])

        else:
            with st.chat_message("assistant", avatar="🌾"):
                st.write(msg["content"])

                # ── SOURCES ──
                if msg.get("sources"):
                    st.caption("📄 Sources:")

                    for s in msg["sources"]:
                        if s.get("url"):
                            st.markdown(f"📄 [{s['source']}]({s['url']})")
                        else:
                            st.markdown(f"📄 {s['source']} (no link)")

                # TTS
                c1, c2, _ = st.columns([1, 1, 6])

                with c1:
                    if st.button("▶ Read", key=f"read_{i}"):
                        components.html(tts_speak(msg["content"], tts_code), height=0)

                with c2:
                    if st.button("⏹ Stop", key=f"stop_{i}"):
                        components.html(tts_stop(), height=0)


# ─────────────────────────────────────────────
# PROCESS QUERY
# ─────────────────────────────────────────────
def process_query(prompt, lang_code, multilingual_rag, retriever):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.spinner("Thinking… / सोच रहा हूँ…"):

        try:
            # ✔ RAG OUTPUT
            answer, query_en, docs = multilingual_rag(prompt)

            # ✔ TRANSLATION
            if lang_code == "hi":
                answer = translate_with_llm(answer, target_lang="hi")

            # ✔ BUILD SOURCES (CSV MAPPING)
            sources = []

            for doc in docs:
                meta = doc.metadata or {}

                file_path = meta.get("source") or meta.get("filename")

                if file_path:
                    filename = os.path.basename(file_path)
                else:
                    filename = "Unknown.pdf"

                url = get_url(filename)

                sources.append({
                    "source": filename,
                    "url": url,
                    "page": meta.get("page", "?")
                })

            # ✔ STORE MESSAGE
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources,
            })

        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": HINDI_ERROR if lang_code == "hi" else str(e),
                "sources": [],
            })

    st.rerun()




