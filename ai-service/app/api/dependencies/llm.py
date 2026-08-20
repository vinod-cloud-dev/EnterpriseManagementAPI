from app.application.interfaces.llm import LLMInterface
from app.core.config.settings import get_settings
from app.infrastructure.llm.factory import create_llm

def get_llm() -> LLMInterface:
    settings = get_settings()
    return create_llm(settings)