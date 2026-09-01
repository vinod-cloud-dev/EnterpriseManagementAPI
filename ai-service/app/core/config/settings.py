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
@lru_cache
def get_settings() -> Settings:
    return Settings()
