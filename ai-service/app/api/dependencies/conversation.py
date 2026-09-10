from fastapi import Depends
from app.application.interfaces.conversation_memory import (
    ConversationMemoryInterface,
)
from app.application.interfaces.llm import LLMInterface
from app.application.interfaces.context_manager import (
    ContextManagerInterface,
)
from app.application.services.conversation_service import (
    ConversationService,
)
from app.api.dependencies.llm import get_llm
from app.api.dependencies.memory import get_memory
from app.api.dependencies.context_manager import get_context_manager
from app.api.dependencies.repository import (
    get_conversation_repository,
)
from app.application.interfaces.conversation_repository import (
    ConversationRepositoryInterface,
)

def get_conversation_service(
    llm: LLMInterface = Depends(get_llm),
    memory: ConversationMemoryInterface = Depends(get_memory),
    context_manager: ContextManagerInterface = Depends(
        get_context_manager
    ),
    repository: ConversationRepositoryInterface = Depends(
        get_conversation_repository
    ),
) -> ConversationService:

    return ConversationService(
        llm=llm,
        memory=memory,
        repository=repository,
        context_manager=context_manager,
    )