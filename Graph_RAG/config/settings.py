"""
Settings and configuration for Graph RAG system
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""
    
    # Neo4j Configuration
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
    
    # LLM Configuration
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-pro")
    LLM_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
    # RAG Configuration
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1024))
    OVERLAP = int(os.getenv("OVERLAP", 100))
    
    # Embedding Configuration
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    
    def __init__(self):
        """Initialize settings"""
        self.validate()
    
    def validate(self):
        """Validate settings"""
        if not self.LLM_API_KEY:
            raise ValueError("LLM_API_KEY not configured")


settings = Settings()
