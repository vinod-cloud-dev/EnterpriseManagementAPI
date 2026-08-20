from fastapi import Depends

from app.application.interfaces.conversation_memory import (
    ConversationMemoryInterface,
)
from app.application.interfaces.llm import LLMInterface
from app.application.services.conversation_service import ConversationService
from app.api.dependencies.llm import get_llm
from app.api.dependencies.memory import get_memory


def get_conversation_service(
    llm: LLMInterface = Depends(get_llm),
    memory: ConversationMemoryInterface = Depends(get_memory),
) -> ConversationService:

    return ConversationService(
        llm=llm,
        memory=memory,
    )