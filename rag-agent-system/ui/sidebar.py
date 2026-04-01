import streamlit as st
import tempfile

from src.loaders.document_loader import load_document
from src.chunking.text_splitter import split_docs
from src.embeddings.embedding_model import get_embeddings
from src.vectorstore.vector_store import create_vectorstore, get_retriever


def sidebar():
    st.sidebar.title("📚 Knowledge Base")

    uploaded_file = st.sidebar.file_uploader(
        "Upload PDF/DOCX", type=["pdf", "docx"]
    )

    if uploaded_file:
        with st.sidebar.spinner("Processing..."):

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.getbuffer())
                file_path = tmp.name

            docs = load_document(file_path, uploaded_file.type)
            chunks = split_docs(docs)

            embeddings = get_embeddings()
            db = create_vectorstore(chunks, embeddings)

            st.session_state.retriever = get_retriever(db)

            st.sidebar.success("✅ Knowledge Base Ready")

    if st.sidebar.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()