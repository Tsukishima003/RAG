import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, model_validator

load_dotenv()

class Settings(BaseSettings):
    # API Info
    APP_TITLE: str = "Real-Time RAG Assistant API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "AI Assistant with RAG using Groq Llama and Chroma Cloud"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENVIRONMENT: str = "development"  # development | staging | production
    LOG_LEVEL: str = "INFO"

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    # Groq AI
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # ChromaDB
    CHROMA_API_KEY: str = os.getenv("CHROMA_API_KEY", "")
    CHROMA_TENANT: str = os.getenv("CHROMA_TENANT", "")
    CHROMA_DATABASE: str = os.getenv("CHROMA_DATABASE", "")
    CHROMA_COLLECTION_NAME: str = "documents"

    # Document Processing
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # File Upload
    UPLOAD_DIRECTORY: Path = Field(default=Path("./uploads"))
    ALLOWED_FILE_EXTENSIONS: list[str] = ['.pdf', '.txt', '.docx', '.doc']
    MAX_FILE_SIZE_MB: int = 50

    # Rate Limiting
    RATE_LIMIT: str = "10/minute"

    # Auth (optional — leave empty to disable)
    API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
settings.UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)