# ─────────────────────────────────────────────
# core/rag.py
# Thin adapter that imports the RAG function and retriever
# from your existing connect_memory_with_llm.py so that the
# rest of the app only ever imports from core.rag.
#
# If you later swap out the underlying RAG implementation,
# only this file needs to change.


#app.py  →  core/rag.py  →  #connect_memory_with_llm.py
#                ↑
#         only this file
#         knows about the
#         legacy module
# ─────────────────────────────────────────────
# core/rag.py

import sys
import os

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# llm is already a module-level variable in connect_memory_with_llm.py
# — no changes needed there, it's directly importable
from connect_memory_with_llm import llm, retriever, rag_chain

__all__ = ["llm", "retriever", "multilingual_rag", "detect_language", "translate_with_llm"]


# ─────────────────────────────────────────────
# Language detection
# ─────────────────────────────────────────────

def detect_language(text: str) -> str:
    """
    Detect if text is Hindi or English.
    Uses Unicode range check (no external library needed):
    Hindi Devanagari block = U+0900 to U+097F.

    Returns 'hi' if enough Hindi characters found, else 'en'.
    """
    hindi_chars = sum(1 for ch in text if '\u0900' <= ch <= '\u097F')
    return "hi" if hindi_chars > 2 else "en"


# ─────────────────────────────────────────────
# RAG  (always runs in English)
# ─────────────────────────────────────────────
'''
def multilingual_rag(query: str):
    """
    Run the RAG pipeline. Always queries in English.

    - If input is Hindi  → translate to English first using LLM
    - RAG runs in English
    - Returns (english_answer, english_query)

    Translation BACK to Hindi is handled separately in ui/chat.py
    so that the UI language setting controls the output language,
    not the input language.

    Returns:
        Tuple of (answer_in_english, query_in_english)
    """
    input_lang = detect_language(query)
    print("Detected ")
    # Translate Hindi query → English using LLM (not deep_translator)
    if input_lang == "hi":
        query_en = _translate_query_to_english(query)
    else:
        query_en = query

    answer_en = rag_chain.invoke(query_en) #This hides retrieval inside the chain.
    return answer_en, query_en
'''

def multilingual_rag(query: str):
    input_lang = detect_language(query)

    print("\n================ NEW QUERY ================")
    print("Original Query:", query)

    # Step 1: Translate if needed
    if input_lang == "hi":
        query_en = _translate_query_to_english(query)
    else:
        query_en = query

    print("English Query:", query_en)

    # Step 2: Retrieve chunks
    docs = retriever.invoke(query_en)

    print("\n🔍 Retrieved Chunks:\n")
    for i, doc in enumerate(docs):
        print(f"----- Chunk {i+1} -----")
        print(doc.page_content)
        print("Metadata:", doc.metadata)
        print("\n")

    # Step 3: Build context
    context = "\n\n".join(doc.page_content for doc in docs)

    print("\n🧠 FULL CONTEXT SENT TO LLM:\n")
    print(context)

    # Step 4: Build final prompt
    full_prompt = f"""
Use the context below to answer the question.

If the question is a single word and you dont have a good context then answer the question by explaining the word meaning . If the answer is not found, say you don't know.if the question is not related to agriculture, say it is not related to the context provided and then ansewr it.but if it is related to agriculture then answer it by using the context provided and directly give the answer you need not to add anything reatad to this prompt.dont give one word answer.

Context:
{context}

Question:
{query_en}

Answer:
"""

    print("\n📤 FINAL PROMPT SENT TO LLM:\n")
    print(full_prompt)

    # Step 5: Call LLM
    response = llm.invoke(full_prompt)

    answer_en = response.content if hasattr(response, "content") else str(response)

    print("\n🤖 FINAL ANSWER:\n")
    print(answer_en)

    return answer_en, query_en,docs




















def _translate_query_to_english(hindi_query: str) -> str:
    """
    Use the project LLM to translate a Hindi query to English.
    Keeps technical terms intact.
    """
    prompt = f"""Translate the following Hindi agriculture question into English.
Keep technical terms like Urea, DAP, NPK, pH, Kharif, Rabi as-is.
Return ONLY the English translation, nothing else.

Hindi question: {hindi_query}

English translation:"""

    response = llm.invoke(prompt)
    if hasattr(response, "content"):
        return response.content.strip()
    return str(response).strip()


# ─────────────────────────────────────────────
# Answer translation  (English → Hindi)
# ─────────────────────────────────────────────

def translate_with_llm(text: str, target_lang: str) -> str:
    """
    Translate an English RAG answer into the target language using the LLM.

    Args:
        text:        English answer from RAG.
        target_lang: 'hi' for Hindi, 'en' to skip translation.

    Returns:
        Translated string, or original if target_lang is 'en'.
    """
    if target_lang == "en":
        return text

    prompt = f"""You are a professional Hindi translator specializing in agriculture.

Translate the following English text into simple, clear Hindi (Devanagari script).

Rules:
- Keep all technical terms in English as-is: Urea, DAP, NPK, SSP, MOP, pH,
  Kharif, Rabi, Zaid, ZnSO4, and any chemical formula or brand name.
- Do NOT translate numbers, units (kg, ha, mg, %) or chemical symbols.
- Write natural Hindi that a farmer can easily understand.
- Return ONLY the Hindi translation, no English alongside it, no explanation.

English text:
{text}

Hindi translation:"""

    response = llm.invoke(prompt)
    if hasattr(response, "content"):
        return response.content.strip()
    return str(response).strip()