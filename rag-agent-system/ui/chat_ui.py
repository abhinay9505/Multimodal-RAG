import streamlit as st

def apply_styles():
    with open("ui/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def display_chat(chat_history):
    if chat_history:
        for msg in chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <div class="user-bubble">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="bot-message">
                    <div class="bot-bubble">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; margin-top:100px; color:gray;">
            <h1>🤖 RAG Chatbot</h1>
            <h3>Upload a document and start chatting</h3>
        </div>
        """, unsafe_allow_html=True)


def chat_input_box():
    return st.chat_input("Type your message...")