from fastapi import Depends
from app.application.interfaces.context_manager import (
    ContextManagerInterface,
)
from app.application.interfaces.context_builder import (
    ContextBuilderInterface,
)
from app.application.interfaces.token_counter import (
    TokenCounterInterface,
)
from app.application.interfaces.conversation_repository import (
    ConversationRepositoryInterface,
)
from app.application.interfaces.conversation_summarizer import (
    ConversationSummarizerInterface,
)

from app.application.services.context_manager import ContextManager

from app.api.dependencies.context_builder import (
    get_context_builder,
)
from app.api.dependencies.summarizer import (
    get_conversation_summarizer,
)
from app.api.dependencies.repository import (
    get_conversation_repository,
)

from app.infrastructure.tokenization.token_counter import TokenCounter
from app.core.config.settings import get_settings
from app.application.interfaces.relevant_message_retriever import (
    RelevantMessageRetriever,
)

from app.api.dependencies.retrieval import (
    get_hybrid_retriever,
)


def get_token_counter() -> TokenCounterInterface:
    return TokenCounter()


def get_context_manager(
    context_builder: ContextBuilderInterface = Depends(
        get_context_builder
    ),
    token_counter: TokenCounterInterface = Depends(
        get_token_counter
    ),
    repository: ConversationRepositoryInterface = Depends(
        get_conversation_repository
    ),
    summarizer: ConversationSummarizerInterface = Depends(
        get_conversation_summarizer
    ),
    relevant_message_retriever: RelevantMessageRetriever = Depends(
    get_hybrid_retriever
),
) -> ContextManagerInterface:

    settings = get_settings()

    return ContextManager(
        context_builder=context_builder,
        token_counter=token_counter,
        repository=repository,
        summarizer=summarizer,
        relevant_message_retriever=relevant_message_retriever,

        max_context_tokens=settings.llm_context_window,
        max_output_tokens=settings.llm_max_output_tokens,
        relevant_message_limit=settings.relevant_message_limit,

    )