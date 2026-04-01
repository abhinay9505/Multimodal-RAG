"""
Streamlit UI for Graph RAG System
"""
import sys
from pathlib import Path

import streamlit as st

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.graph_rag import GraphRAG


def initialize_session():
    """Initialize session state"""
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = GraphRAG()
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []


def main():
    """Main Streamlit application"""
    st.set_page_config(page_title="Graph RAG System", layout="wide")
    
    initialize_session()
    
    st.title("🔍 Graph RAG System")
    st.markdown("Retrieval Augmented Generation using Knowledge Graphs")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Document upload
        uploaded_file = st.file_uploader("Upload documents", type=['txt', 'pdf'])
        if uploaded_file:
            st.success("Document uploaded!")
        
        # Model selection
        model = st.selectbox("Select LLM Model", ["gpt-4", "gpt-3.5-turbo"])
        
        # Clear history
        if st.button("Clear Conversation"):
            st.session_state.conversation_history = []
    
    # Main chat interface
    st.subheader("Chat with your documents")
    
    # Display conversation history
    for message in st.session_state.conversation_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input for new query
    user_input = st.chat_input("Ask a question about your documents...")
    
    if user_input:
        # Add user message
        st.session_state.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.rag_system.query(user_input)
                st.markdown(response)
        
        # Add assistant message
        st.session_state.conversation_history.append({
            "role": "assistant",
            "content": response
        })


if __name__ == "__main__":
    main()
