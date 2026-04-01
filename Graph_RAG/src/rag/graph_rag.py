"""
Graph RAG Pipeline
Implements Retrieval Augmented Generation using Knowledge Graph
"""
from typing import List, Dict, Any, Optional
from src.graph.neo4j_manager import Neo4jManager
from src.llm.llm_manager import LLMManager
from src.loaders.document_loader import DocumentLoader
from config.settings import settings


class GraphRAG:
    """Graph-based Retrieval Augmented Generation system"""
    
    def __init__(self, graph_manager: Optional[Neo4jManager] = None,
                 llm_manager: Optional[LLMManager] = None):
        """
        Initialize Graph RAG system
        
        Args:
            graph_manager: Neo4j manager instance
            llm_manager: LLM manager instance
        """
        self.graph = graph_manager or Neo4jManager()
        self.llm = llm_manager or LLMManager()
    
    def ingest_documents(self, documents: List[str]) -> None:
        """
        Ingest documents into the knowledge graph
        
        Args:
            documents: List of documents to ingest
        """
        for i, doc in enumerate(documents):
            # Create document node
            doc_node = self.graph.create_node(
                "Document",
                {"id": i, "content": doc, "title": f"doc_{i}"}
            )
            
            # Extract entities and create relationships
            entities = self.extract_entities(doc)
            for entity in entities:
                self.graph.create_node(
                    "Entity",
                    {"name": entity["text"], "type": entity["type"]}
                )
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract entities from text
        
        Args:
            text: Input text
            
        Returns:
            List of entities
        """
        return self.llm.extract_entities(text)
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: Query string
            top_k: Number of results to return
            
        Returns:
            List of retrieved documents/contexts
        """
        # Convert query to embedding
        query_embedding = self.llm.generate_embeddings(query)
        
        # Query graph for relevant nodes
        cypher_query = """
        MATCH (d:Document)
        RETURN d LIMIT $limit
        """
        
        results = self.graph.query(cypher_query, {"limit": top_k})
        return results
    
    def generate_answer(self, query: str, context: List[str]) -> str:
        """
        Generate answer based on query and context
        
        Args:
            query: User query
            context: Retrieved context
            
        Returns:
            Generated answer
        """
        context_text = "\n".join(context)
        prompt = f"""
        Context: {context_text}
        
        Question: {query}
        
        Answer:
        """
        
        return self.llm.generate_response(prompt)
    
    def query(self, query: str) -> str:
        """
        Full RAG pipeline: retrieve and generate
        
        Args:
            query: User query
            
        Returns:
            Generated response
        """
        # Retrieve relevant documents
        retrieved = self.retrieve(query)
        
        # Extract context
        context = [doc.get("content", "") for doc in retrieved]
        
        # Generate answer
        answer = self.generate_answer(query, context)
        
        return answer
    
    def close(self):
        """Close connections"""
        self.graph.close()
