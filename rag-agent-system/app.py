import streamlit as st

from ui.chat_ui import apply_styles, display_chat, chat_input_box
from ui.sidebar import sidebar

from src.llm.groq_llm import load_llm
from src.chains.rag_chain import build_rag_chain
from src.utils.helpers import format_docs

# Page config
st.set_page_config(page_title="RAG Chatbot", layout="wide")

# Apply styles
apply_styles()

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "retriever" not in st.session_state:
    st.session_state.retriever = None

# Sidebar
sidebar()

# Display chat
display_chat(st.session_state.chat_history)

# Input
user_input = chat_input_box()

if user_input:
    if not st.session_state.retriever:
        st.error("⚠️ Upload document first")
    else:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        with st.spinner("Thinking..."):
            model = load_llm()

            rag_chain = build_rag_chain(
                st.session_state.retriever,
                model,
                format_docs
            )

            response = rag_chain.invoke(user_input)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })

        st.rerun()