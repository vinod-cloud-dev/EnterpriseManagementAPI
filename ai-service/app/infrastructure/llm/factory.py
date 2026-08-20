from app.application.interfaces.llm import LLMInterface
from app.core.config.settings import Settings
from app.infrastructure.llm.ollama_client import OllamaClient


def create_llm(settings: Settings) -> LLMInterface:
    if settings.llm_provider == "ollama":
        return OllamaClient(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
        )
    raise ValueError( f"Unsupported LLM provider: {settings.llm_provider}" )