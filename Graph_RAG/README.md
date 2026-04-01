# Graph RAG System

A knowledge graph-based Retrieval Augmented Generation system powered by Google Gemini API and Neo4j.

## Features

- **Knowledge Graph Integration**: Uses Neo4j for storing and querying knowledge graphs
- **Google Gemini LLM**: Leverages Google's Gemini models for text generation and understanding
- **Document Processing**: Load and process documents from various formats (PDF, TXT)
- **Entity Extraction**: Automatically extract entities from documents
- **Semantic Search**: Find relevant documents based on semantic similarity
- **Streamlit UI**: Interactive web interface for querying documents

## Installation

1. Clone the repository:
```bash
git clone https://github.com/abhinay9505/Multimodal-RAG.git
cd Graph_RAG
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following:
```env
GOOGLE_API_KEY=your_google_api_key
NEO4J_URI=neo4j+s://your-neo4j-uri
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
```

## Usage

### Running the Streamlit UI

```bash
streamlit run ui/app.py
```

### Using the Graph RAG programmatically

```python
from src.rag.graph_rag import GraphRAG
from src.loaders.document_loader import TextLoader, DirectoryLoader

# Initialize the system
rag = GraphRAG()

# Load documents
loader = TextLoader()
docs = loader.load("path/to/document.txt")

# Ingest documents
rag.ingest_documents(docs)

# Query the system
response = rag.query("What is the main topic?")
print(response)
```

## Project Structure

```
Graph_RAG/
├── config/
│   ├── settings.py         # Configuration settings
│   └── __init__.py
├── src/
│   ├── graph/
│   │   ├── neo4j_manager.py
│   │   └── __init__.py
│   ├── llm/
│   │   ├── llm_manager.py  # Google Gemini integration
│   │   └── __init__.py
│   ├── loaders/
│   │   ├── document_loader.py
│   │   └── __init__.py
│   └── rag/
│       ├── graph_rag.py    # Main RAG pipeline
│       └── __init__.py
├── ui/
│   ├── app.py              # Streamlit application
│   └── __init__.py
├── requirements.txt
└── .env
```

## Components

### LLMManager
Handles all interactions with Google Gemini API:
- Text generation
- Entity extraction
- Embeddings generation
- Text summarization

### Neo4jManager
Manages Neo4j graph database operations:
- Node creation
- Relationship creation
- Custom queries
- Graph manipulation

### DocumentLoader
Loads documents from various sources:
- PDF files
- Text files
- Multiple files from a directory

### GraphRAG
Main RAG pipeline orchestrating:
- Document ingestion
- Entity extraction
- Document retrieval
- Answer generation

## API Keys Required

- **Google API Key**: Get from [Google Cloud Console](https://console.cloud.google.com/)
- **Neo4j**: Set up Neo4j instance (local or cloud)

## License

MIT License
