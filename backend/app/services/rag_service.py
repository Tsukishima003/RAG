from app.core.rag_engine import RAGEngine
from app.config.settings import settings


class RAGService:
    """Singleton wrapper for RAG Engine"""
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> RAGEngine:
        """Get or create RAG Engine instance"""
        if cls._instance is None:
            cls._instance = RAGEngine(
                groq_api_key=settings.GROQ_API_KEY,
                model_name=settings.GROQ_MODEL,
                collection_name=settings.CHROMA_COLLECTION_NAME,
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                cloud_api_key=settings.CHROMA_API_KEY,
                cloud_tenant=settings.CHROMA_TENANT,
                cloud_database=settings.CHROMA_DATABASE,
            )
        return cls._instance
    
    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance (useful for testing)"""
        cls._instance = None


# Global RAG service instance
rag_service = RAGService.get_instance()
