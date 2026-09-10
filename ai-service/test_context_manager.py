import asyncio
from uuid import uuid4
from datetime import datetime, timezone

from app.application.services.context_manager import ContextManager
from app.application.services.conversation_summarizer import ConversationSummarizer
from app.infrastructure.tokenization.token_counter import TokenCounter
from app.api.dependencies.llm import get_llm
from app.api.dependencies.context_builder import get_context_builder
from uuid import UUID, uuid4
from app.infrastructure.database.database import AsyncSessionLocal
from app.infrastructure.database.repositories.conversation_repository import (
    ConversationRepository,
)

from app.domain.models.conversation_message import ConversationMessage




async def main():

    print("Creating dependencies...\n")

    # LLM
    llm = get_llm()

    # Context Builder
    context_builder = get_context_builder()

    # Token Counter
    token_counter = TokenCounter()

    conversation_id = UUID("6b851f2b-025f-4cca-a471-083d5fe61635")
    # ---------------------------------------------------------
    # Create real database session
    # ---------------------------------------------------------

    async with AsyncSessionLocal() as session:

        # Repository
        repository = ConversationRepository(session)

        existing = await repository.get_conversation(
            conversation_id=conversation_id,
            user_id=1,
        )

        if not existing:
            await repository.create_conversation(
                conversation_id=conversation_id,
                user_id=1,
            )

        # Summarizer
        summarizer = ConversationSummarizer(llm)

        # Create ContextManager
        context_manager = ContextManager(
            context_builder=context_builder,
            token_counter=token_counter,
            repository=repository,
            summarizer=summarizer,
            max_context_tokens=100,
            max_output_tokens=300,
        )

        # ---------------------------------------------------------
        # Create test conversation history
        # ---------------------------------------------------------

        messages = []

        for i in range(1, 11):

            messages.append(
                ConversationMessage(
                    id=uuid4(),
                    conversation_id=conversation_id,
                    role="user" if i % 2 != 0 else "assistant",
                    content=(
                        f"This is test conversation message number {i}. "
                        "Vinod is building an Employee AI platform using "
                        "FastAPI, PostgreSQL, Redis, Ollama and a local LLM. "
                        "The architecture should support conversation "
                        "summarization, RAG, embeddings, agents and tools."
                    ),
                    created_at=datetime.now(timezone.utc),
                    sequence_number=i,
                )
            )

        current_message = (
            "Tell me what you remember about this Employee AI project "
            "and the important architectural decisions."
        )

        print("Conversation ID:")
        print(conversation_id)

        print("\nNumber of history messages:")
        print(len(messages))

        print("\nCalling ContextManager...\n")

        # ---------------------------------------------------------
        # Build Context
        # ---------------------------------------------------------

        context = await context_manager.build_context(
            conversation_id=conversation_id,
            history=messages,
            current_message=current_message,
        )

        print("\n========== FINAL CONTEXT ==========\n")
        print(context)
        print("\n===================================\n")


if __name__ == "__main__":
    asyncio.run(main())
