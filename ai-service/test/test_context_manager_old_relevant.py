
import asyncio
from datetime import datetime, timezone
from uuid import uuid4

from app.core.config.settings import get_settings

from app.infrastructure.database.database import AsyncSessionLocal
from app.infrastructure.database.repositories.conversation_repository import (
    ConversationRepository,
)

from app.application.services.context_manager import ContextManager
from app.application.services.context_builder import ContextBuilder
from app.application.services.conversation_summarizer import (
    ConversationSummarizer,
)
from app.application.services.relevant_message_retriever import (
    BasicRelevantMessageRetriever,
)

from app.infrastructure.llm.ollama_client import OllamaClient
from app.infrastructure.tokenization.token_counter import TokenCounter

from app.domain.models.conversation_message import ConversationMessage


async def main() -> None:

    print("Creating dependencies...\n")

    settings = get_settings()

    conversation_id = uuid4()

    print("Conversation ID:")
    print(conversation_id)
    print()

    async with AsyncSessionLocal() as session:

        repository = ConversationRepository(session)

        # --------------------------------------------------
        # Create conversation
        # --------------------------------------------------

        await repository.create_conversation(
            conversation_id=conversation_id,
            user_id=1,
        )

        print("Conversation created.")
        print()

        # --------------------------------------------------
        # Create dependencies
        # --------------------------------------------------

        context_builder = ContextBuilder()

        token_counter = TokenCounter()

        llm = OllamaClient(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
        )

        summarizer = ConversationSummarizer(
            llm=llm,
        )

        relevant_message_retriever = BasicRelevantMessageRetriever(
            repository=repository,
        )

        context_manager = ContextManager(
            context_builder=context_builder,
            token_counter=token_counter,
            repository=repository,
            summarizer=summarizer,
            relevant_message_retriever=relevant_message_retriever,
            max_context_tokens=100,
            max_output_tokens=20,
            relevant_message_limit=settings.relevant_message_limit,
        )

        # --------------------------------------------------
        # Insert old relevant message
        # --------------------------------------------------

        old_message = ConversationMessage(
            id=uuid4(),
            conversation_id=conversation_id,
            role="user",
            content=(
                "The Employee AI project uses PostgreSQL as "
                "the source of truth for persistent conversation "
                "data. Redis is used as a fast cache."
            ),
            sequence_number=1,
            created_at=datetime.now(timezone.utc),
        )

        await repository.save_message(old_message)

        print("Inserted old relevant message.")
        print()

        # --------------------------------------------------
        # Insert recent unrelated messages
        # --------------------------------------------------

        recent_messages = [
            (
                "The employee dashboard should show "
                "important notifications."
            ),
            (
                "The notification service should send "
                "real time updates."
            ),
            (
                "The dashboard should display employee "
                "activity information."
            ),
            (
                "The application should expose health "
                "check endpoints."
            ),
            (
                "The API should use structured logging "
                "for debugging."
            ),
            (
                "The project should use clean architecture "
                "and loose coupling."
            ),
            (
                "The application should support scalable "
                "service boundaries."
            ),
            (
                "The AI service should remain independent "
                "from the notification service."
            ),
            (
                "Agents and tools can be added later."
            ),
            (
                "The system should be easy to extend "
                "in the future."
            ),
        ]

        sequence_number = 2

        for content in recent_messages:

            message = ConversationMessage(
                id=uuid4(),
                conversation_id=conversation_id,
                role="user",
                content=content,
                sequence_number=sequence_number,
                created_at=datetime.now(timezone.utc),
            )

            await repository.save_message(message)

            sequence_number += 1

        print(
            f"Inserted {len(recent_messages)} recent unrelated messages."
        )
        print()

        # --------------------------------------------------
        # Current user question
        # --------------------------------------------------

        current_message = (
            "Tell me about PostgreSQL as the source of truth "
            "and Redis as the cache in this Employee AI project."
        )

        print("Current question:")
        print(current_message)
        print()

        # --------------------------------------------------
        # Get history
        # --------------------------------------------------

        history = await repository.get_history(
            conversation_id
        )

        print(
            f"History messages retrieved: {len(history)}"
        )
        print()

        # --------------------------------------------------
        # Test retriever independently
        # --------------------------------------------------

        print("Testing relevant message retriever...\n")

        relevant_results = (
            await relevant_message_retriever.retrieve(
                conversation_id=conversation_id,
                query=current_message,
               limit=settings.relevant_message_limit,
            )
        )

        print("========== RETRIEVER RESULTS ==========")

        for result in relevant_results:

            print(
                f"Sequence: {result.message.sequence_number}"
            )

            print(
                f"Score: {result.relevance_score}"
            )

            print(
                f"Source: {result.retrieval_source}"
            )

            print(
                f"Content: {result.message.content}"
            )

            print("----------------------------------------")

        print("========================================\n")

        # --------------------------------------------------
        # Build context
        # --------------------------------------------------

        print("Calling ContextManager...\n")

        final_context = await context_manager.build_context(
            conversation_id=conversation_id,
            history=history,
            current_message=current_message,
        )

        # --------------------------------------------------
        # Print final context
        # --------------------------------------------------

        print("\n========== FINAL CONTEXT ==========\n")

        print(final_context)

        print("\n===================================\n")

        # --------------------------------------------------
        # Verification
        # --------------------------------------------------

        context_lower = final_context.lower()

        has_relevant_section = (
            "relevant conversation:" in context_lower
        )

        has_postgres = (
            "postgresql" in context_lower
        )

        has_redis = (
            "redis" in context_lower
        )

        has_summary = (
            "conversation summary:" in context_lower
        )

        print("\n========== VERIFICATION ==========")

        # --------------------------------------------------
        # Relevant message section
        # --------------------------------------------------

        if has_relevant_section:

            print(
                "PASS: Relevant conversation section found."
            )

        else:

            print(
                "INFO: Relevant messages did not fit "
                "the token budget; summary fallback was used."
            )

        # --------------------------------------------------
        # PostgreSQL verification
        # --------------------------------------------------

        if has_postgres:

            print(
                "PASS: PostgreSQL context is preserved."
            )

        else:

            print(
                "FAIL: PostgreSQL context is missing."
            )

        # --------------------------------------------------
        # Redis verification
        # --------------------------------------------------

        if has_redis:

            print(
                "PASS: Redis context is preserved."
            )

        else:

            print(
                "FAIL: Redis context is missing."
            )

        # --------------------------------------------------
        # Summary fallback verification
        # --------------------------------------------------

        if (
            not has_relevant_section
            and has_summary
            and has_postgres
            and has_redis
        ):

            print(
                "PASS: Relevant information was preserved "
                "through summary fallback."
            )

        # --------------------------------------------------
        # Final result
        # --------------------------------------------------

        if has_postgres and has_redis:

            print(
                "\nPASS: ContextManager preserved the "
                "important PostgreSQL and Redis information."
            )

        else:

            print(
                "\nFAIL: Important conversation information "
                "was lost."
            )

        print("=================================\n")


if __name__ == "__main__":
    asyncio.run(main())
