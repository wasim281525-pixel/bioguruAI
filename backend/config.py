from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "BioGuru AI"
    SECRET_KEY: str = "change-me-in-production-use-a-long-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # LLM
    ANTHROPIC_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    LLM_PROVIDER: str = "anthropic"  # anthropic | groq
    LLM_MODEL: str = "claude-sonnet-4-20250514"

    # Embeddings
    EMBEDDING_MODEL: str = "intfloat/multilingual-e5-large"

    # Vector DB
    VECTOR_DB: str = "chroma"  # chroma | pinecone | faiss
    CHROMA_HOST: str = "chroma"
    CHROMA_PORT: int = 8000

    PINECONE_API_KEY: str = ""
    PINECONE_INDEX: str = "bioguru"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://bioguru:bioguru@postgres:5432/bioguru"
    REDIS_URL: str = "redis://redis:6379"

    # Storage
    S3_BUCKET: str = ""
    AWS_ACCESS_KEY: str = ""
    AWS_SECRET_KEY: str = ""

    # Voice
    WHISPER_MODEL: str = "whisper-1"
    OPENAI_API_KEY: str = ""

    # Retrieval
    TOP_K: int = 5
    SIMILARITY_THRESHOLD: float = 0.5
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 64

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 30
    RATE_LIMIT_WINDOW: int = 60

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "https://bioguru.ai"]

    class Config:
        env_file = ".env"


settings = Settings()
