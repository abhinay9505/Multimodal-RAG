from langchain_groq import ChatGroq
from config.settings import GROQ_API_KEY, GROQ_MODEL

def load_llm():
    return ChatGroq(
        model=GROQ_MODEL,
        groq_api_key=GROQ_API_KEY
    )