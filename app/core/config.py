"""Application configuration management."""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Application
    APP_NAME: str = "Social Media Analytics AI Agent"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # API
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # LLM Providers
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    LLM_PROVIDER: str = "openai"
    LLM_MODEL: str = "gpt-4-turbo-preview"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 2000

    # Vector Store
    VECTOR_STORE_TYPE: str = "chroma"
    CHROMA_PERSIST_DIRECTORY: str = "./data/chroma"
    EMBEDDING_MODEL: str = "sentence-transformers/all-mpnet-base-v2"

    # Agent Configuration
    AGENT_MAX_ITERATIONS: int = 10
    AGENT_MAX_EXECUTION_TIME: int = 300
    CONVERSATION_MEMORY_SIZE: int = 10

    # Social Media Mock Data
    ENABLE_MOCK_DATA: bool = True
    MOCK_DATA_REFRESH_INTERVAL: int = 300

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
