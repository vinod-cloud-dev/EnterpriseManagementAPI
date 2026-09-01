from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.application.interfaces.conversation_memory import (ConversationMemoryInterface,)
from app.application.interfaces.llm import LLMInterface
from app.application.services.conversation_service import ConversationService
from app.api.dependencies.llm import get_llm
from app.api.dependencies.memory import get_memory
from app.api.dependencies.context_builder import get_context_builder
from app.application.interfaces.context_builder import ( ContextBuilderInterface,)
from app.infrastructure.database.database import get_db
from app.infrastructure.database.repositories.conversation_repository import (ConversationRepository,)

def get_conversation_service(
    llm: LLMInterface = Depends(get_llm),
    memory: ConversationMemoryInterface = Depends(get_memory),
    context_builder: ContextBuilderInterface = Depends(get_context_builder),
    session: AsyncSession = Depends(get_db),
) -> ConversationService:
    
    repository = ConversationRepository(session)
    return ConversationService(
        llm=llm,
        memory=memory,
         repository=repository,
        context_builder=context_builder,
    )