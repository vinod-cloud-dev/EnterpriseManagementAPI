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

@lru_cache
def get_settings() -> Settings:
    return Settings()
