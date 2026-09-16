"""Environment-based application configuration."""

import os
from dataclasses import dataclass
from functools import lru_cache
from dotenv import load_dotenv
load_dotenv()

@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Employee AI Service")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    environment: str = os.getenv("ENVIRONMENT", "development")
    llm_provider: str = os.getenv("LLM_PROVIDER", "ollama")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL","http://localhost:11434",)
    ollama_model: str = os.getenv("OLLAMA_MODEL","qwen3:1.7b",)
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_user: str = os.getenv("POSTGRES_USER", "ai_user")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "")
    postgres_db: str = os.getenv("POSTGRES_DB", "employee_ai")
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")
    jwt_issuer: str = os.getenv("JWT_ISSUER", "Employee_Proj")
    jwt_audience: str = os.getenv("JWT_AUDIENCE", "EmployeeAPIUsers")
    llm_context_window: int = int(os.getenv("LLM_CONTEXT_WINDOW", "8192"))
    llm_max_output_tokens: int = int(os.getenv("LLM_MAX_OUTPUT_TOKENS", "1500"))
    relevant_message_limit: int = int(os.getenv("RELEVANT_MESSAGE_LIMIT", "3"))
    #Embedding models
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-0.6B")
    hybrid_semantic_weight: float = float(os.getenv("HYBRID_SEMANTIC_WEIGHT", "0.7"))
    hybrid_keyword_weight: float = float(os.getenv("HYBRID_KEYWORD_WEIGHT", "0.3"))
    def __post_init__(self) -> None:
        if not 0.0 <= self.hybrid_semantic_weight <= 1.0:
            raise ValueError(
                "HYBRID_SEMANTIC_WEIGHT must be between 0.0 and 1.0"
            )

        if not 0.0 <= self.hybrid_keyword_weight <= 1.0:
            raise ValueError(
                "HYBRID_KEYWORD_WEIGHT must be between 0.0 and 1.0"
            )

        if abs(
            (self.hybrid_semantic_weight + self.hybrid_keyword_weight) - 1.0
        ) > 0.000001:
            raise ValueError(
                "HYBRID_SEMANTIC_WEIGHT + HYBRID_KEYWORD_WEIGHT must equal 1.0"
            )
@lru_cache
def get_settings() -> Settings:
    return Settings()
