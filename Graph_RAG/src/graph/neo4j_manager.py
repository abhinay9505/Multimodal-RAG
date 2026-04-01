"""
Neo4j Graph Database Manager
Handles all graph database operations
"""
from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase, Session
from config.settings import settings


class Neo4jManager:
    """Manager for Neo4j graph database operations"""
    
    def __init__(self, uri: str = settings.NEO4J_URI, 
                 username: str = settings.NEO4J_USERNAME,
                 password: str = settings.NEO4J_PASSWORD):
        """
        Initialize Neo4j manager
        
        Args:
            uri: Neo4j connection URI
            username: Neo4j username
            password: Neo4j password
        """
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
    
    def close(self):
        """Close database connection"""
        if self.driver:
            self.driver.close()
    
    def create_node(self, label: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a node in the graph
        
        Args:
            label: Node label
            properties: Node properties
            
        Returns:
            Created node details
        """
        with self.driver.session() as session:
            result = session.run(
                f"CREATE (n:{label} $properties) RETURN n",
                properties=properties
            )
            return result.single()
    
    def create_relationship(self, from_node_id: str, to_node_id: str, 
                          relation_type: str, properties: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create a relationship between two nodes
        
        Args:
            from_node_id: Source node ID
            to_node_id: Target node ID
            relation_type: Type of relationship
            properties: Optional relationship properties
            
        Returns:
            Relationship details
        """
        with self.driver.session() as session:
            props = properties or {}
            result = session.run(
                f"MATCH (a), (b) WHERE id(a)=$from_id AND id(b)=$to_id "
                f"CREATE (a)-[r:{relation_type} $props]->(b) RETURN r",
                from_id=from_node_id,
                to_id=to_node_id,
                props=props
            )
            return result.single()
    
    def query(self, query_str: str, parameters: Optional[Dict] = None) -> List[Dict]:
        """
        Execute custom query
        
        Args:
            query_str: Cypher query string
            parameters: Query parameters
            
        Returns:
            Query results
        """
        with self.driver.session() as session:
            result = session.run(query_str, parameters=parameters or {})
            return [record.data() for record in result]
    
    def delete_all(self):
        """Delete all nodes and relationships"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
