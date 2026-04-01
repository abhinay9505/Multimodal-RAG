"""
Document Loader
Handles loading documents from various sources
"""
from typing import List, Optional
from pathlib import Path


class DocumentLoader:
    """Base document loader class"""
    
    def load(self, path: str) -> List[str]:
        """
        Load documents from path
        
        Args:
            path: Path to document(s)
            
        Returns:
            List of document contents
        """
        raise NotImplementedError("Subclasses must implement load()")


class PDFLoader(DocumentLoader):
    """PDF document loader"""
    
    def load(self, path: str) -> List[str]:
        """
        Load PDF documents
        
        Args:
            path: Path to PDF file
            
        Returns:
            List of extracted text from PDF
        """
        try:
            from PyPDF2 import PdfReader
            documents = []
            pdf_path = Path(path)
            
            if pdf_path.is_file():
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    documents.append(page.extract_text())
            
            return documents
        except ImportError:
            raise ImportError("PyPDF2 not installed. Install with: pip install PyPDF2")


class TextLoader(DocumentLoader):
    """Text document loader"""
    
    def load(self, path: str) -> List[str]:
        """
        Load text documents
        
        Args:
            path: Path to text file
            
        Returns:
            List with single document content
        """
        path_obj = Path(path)
        
        if path_obj.is_file():
            with open(path_obj, 'r', encoding='utf-8') as f:
                return [f.read()]
        
        return []


class DirectoryLoader:
    """Load all documents from a directory"""
    
    def __init__(self, loader: DocumentLoader, extension: str = "*.txt"):
        """
        Initialize directory loader
        
        Args:
            loader: Document loader instance
            extension: File extension pattern
        """
        self.loader = loader
        self.extension = extension
    
    def load(self, directory: str) -> List[str]:
        """
        Load all documents from directory
        
        Args:
            directory: Directory path
            
        Returns:
            List of all loaded documents
        """
        path = Path(directory)
        documents = []
        
        for file in path.glob(self.extension):
            documents.extend(self.loader.load(str(file)))
        
        return documents
