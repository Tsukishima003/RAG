import os 
from typing import Dict, AsyncGenerator
from app.core.embeddings import create_embeddings
from app.core.vector_store import VectorStore
from app.core.llm import create_llm
from app.core.document_loader import load_document
from app.core.text_processor import TextProcessor
from app.core.query_engine import QueryEngine

class RAGEngine:
    """Main RAG Engine that coordinates all components"""
    
    def __init__(
        self,
        groq_api_key: str,
        model_name: str = "llama-3.1-70b-versatile",
        collection_name: str = "RAGGG",
        cloud_api_key: str = os.getenv("CHROMA_API_KEY"),
        cloud_tenant: str = os.getenv("CHROMA_TENANT"),
        cloud_database: str = os.getenv("CHROMA_DATABASE"),
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        """
        Initialize RAG Engine
        
        Args:
            groq_api_key: Groq API key
            model_name: LLM model name
            collection_name: Collection name
            cloud_api_key: Chroma Cloud API key
            cloud_tenant: Chroma Cloud tenant ID
            cloud_database: Chroma Cloud database name
            chunk_size: Text chunk size
            chunk_overlap: Chunk overlap
        """
        self.groq_api_key = groq_api_key
        self.model_name = model_name
        
        # Initialize components
        self.embeddings = create_embeddings()
        self.vector_store = VectorStore(
            embeddings=self.embeddings,
            collection_name=collection_name,
            cloud_api_key=cloud_api_key,
            cloud_tenant=cloud_tenant,
            cloud_database=cloud_database,
        )
        self.llm = create_llm(groq_api_key, model_name)
        self.text_processor = TextProcessor(chunk_size, chunk_overlap)
        self.query_engine = QueryEngine(self.llm, self.vector_store, groq_api_key, model_name)
    
    def process_document(self, file_path: str) -> int:
        """
        Process and add document to vector store
        
        Args:
            file_path: Path to document
        
        Returns:
            int: Number of chunks created
        """
        # Load document
        documents = load_document(file_path)
        
        # Split into chunks
        chunks = self.text_processor.split_documents(documents)
        
        # Add to vector store
        self.vector_store.add_documents(chunks)
        
        return len(chunks)
    
    def query(self, question: str, chat_history: str = "") -> Dict:
        """
        Query the RAG system (non-streaming)
        
        Args:
            question: User question
            chat_history: Formatted conversation history
        
        Returns:
            Dict: Answer and sources
        """
        return self.query_engine.query(question, chat_history=chat_history)
    
    async def query_stream(self, question: str, chat_history: str = "") -> AsyncGenerator[Dict, None]:
        """
        Query the RAG system with streaming response
        
        Args:
            question: User question
            chat_history: Formatted conversation history
        
        Yields:
            Dict: Streaming response chunks
        """
        async for chunk in self.query_engine.query_stream(question, chat_history=chat_history):
            yield chunk
    
    def get_document_count(self) -> int:
        """Get number of documents in vector store"""
        return self.vector_store.get_document_count()
    
    def clear_documents(self):
        """Clear all documents from vector store"""
        self.vector_store.clear()
