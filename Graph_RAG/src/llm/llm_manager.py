"""
LLM Manager
Handles language model operations using Google Gemini API via LangChain
"""
from typing import List, Optional, Dict, Any
import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain.schema import HumanMessage
from config.settings import settings


class LLMManager:
    """Manager for language model operations using Google Gemini via LangChain"""
    
    def __init__(self, model: str = settings.LLM_MODEL, 
                 api_key: str = settings.LLM_API_KEY):
        """
        Initialize LLM manager with Google Gemini API via LangChain
        
        Args:
            model: Google model name (e.g., 'gemini-1.5-pro', 'gemini-pro')
            api_key: Google API key
        """
        self.model = model
        self.api_key = api_key
        
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not configured")
        
        # Initialize LangChain ChatGoogleGenerativeAI
        self.client = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=0.7,
            convert_system_message_to_human=True
        )
        
        # Initialize embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )
    
    def generate_response(self, prompt: str, max_tokens: int = 500,
                         temperature: float = 0.7) -> str:
        """
        Generate response using Google Gemini via LangChain
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens in response
            temperature: Temperature for generation (0-1)
            
        Returns:
            Generated response
        """
        try:
            # Create a client with custom temperature if needed
            client = ChatGoogleGenerativeAI(
                model=self.model,
                google_api_key=self.api_key,
                temperature=temperature,
                convert_system_message_to_human=True,
                max_output_tokens=max_tokens
            )
            
            message = HumanMessage(content=prompt)
            response = client.invoke([message])
            return response.content
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract entities from text using Google Gemini via LangChain
        
        Args:
            text: Input text
            
        Returns:
            List of extracted entities with types
        """
        prompt = f"""Extract all named entities from the following text. 
        Return as a list of dictionaries with 'text' and 'type' fields.
        
        Text: {text}
        
        Format your response as JSON array."""
        
        try:
            response = self.generate_response(prompt, max_tokens=500)
            
            # Extract JSON from response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                entities = json.loads(json_match.group())
                return entities
            return []
        except Exception as e:
            print(f"Error extracting entities: {e}")
            return []
    
    def generate_embeddings(self, text: str) -> List[float]:
        """
        Generate embeddings using Google Embedding API via LangChain
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        try:
            embedding = self.embeddings.embed_query(text)
            return embedding
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return []
    
    def summarize(self, text: str, max_length: int = 150) -> str:
        """
        Summarize text using Google Gemini via LangChain
        
        Args:
            text: Text to summarize
            max_length: Maximum summary length (approximate)
            
        Returns:
            Summarized text
        """
        prompt = f"""Summarize the following text in approximately {max_length} characters or less.
        
        Text: {text}
        
        Summary:"""
        
        try:
            return self.generate_response(prompt, max_tokens=int(max_length/4))
        except Exception as e:
            print(f"Error summarizing: {e}")
            return ""
