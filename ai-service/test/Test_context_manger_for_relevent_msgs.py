import asyncio
from uuid import uuid4
from datetime import datetime, timezone

from app.application.services.context_manager import ContextManager
from app.application.services.conversation_summarizer import (
    ConversationSummarizer,
)
from app.application.services.relevant_message_retriever import (
    BasicRelevantMessageRetriever,
)

from app.infrastructure.tokenization.token_counter import TokenCounter

from app.api.dependencies.llm import get_llm
from app.api.dependencies.context_builder import get_context_builder

from app.infrastructure.database.database import AsyncSessionLocal
from app.infrastructure.database.repositories.conversation_repository import (
    ConversationRepository,
)

from app.domain.models.conversation_message import ConversationMessage


async def main():

    print("Creating dependencies...\n")

    # ---------------------------------------------------------
    # Dependencies
    # ---------------------------------------------------------

    llm = get_llm()

    context_builder = get_context_builder()

    token_counter = TokenCounter()

    # ---------------------------------------------------------
    # Create a NEW conversation every test run
    # ---------------------------------------------------------

    conversation_id = uuid4()

    # ---------------------------------------------------------
    # Database session
    # ---------------------------------------------------------

    async with AsyncSessionLocal() as session:

        repository = ConversationRepository(session)

        # -----------------------------------------------------
        # Create conversation
        # -----------------------------------------------------

        await repository.create_conversation(
            conversation_id=conversation_id,
            user_id=1,
        )

        # -----------------------------------------------------
        # Create Retriever
        # -----------------------------------------------------

        relevant_message_retriever = (
            BasicRelevantMessageRetriever(
                repository
            )
        )

        # -----------------------------------------------------
        # Create Summarizer
        # -----------------------------------------------------

        summarizer = ConversationSummarizer(llm)

        # -----------------------------------------------------
        # Create ContextManager
        # -----------------------------------------------------

        context_manager = ContextManager(
            context_builder=context_builder,
            token_counter=token_counter,
            repository=repository,
            summarizer=summarizer,
            relevant_message_retriever=relevant_message_retriever,
            max_context_tokens=1000,
            max_output_tokens=300,
        )

        # -----------------------------------------------------
        # Create and SAVE test conversation history
        # -----------------------------------------------------

        messages = []

        for i in range(1, 11):

            message = ConversationMessage(
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

            messages.append(message)

            await repository.save_message(message)

        # -----------------------------------------------------
        # Current user message
        # -----------------------------------------------------

        current_message = (
            "Tell me about FastAPI and PostgreSQL "
            "in this Employee AI project."
        )

        # -----------------------------------------------------
        # Display information
        # -----------------------------------------------------

        print("Conversation ID:")
        print(conversation_id)

        print("\nNumber of history messages:")
        print(len(messages))

        # -----------------------------------------------------
        # Test Retriever DIRECTLY
        # -----------------------------------------------------

        print("\nCalling RelevantMessageRetriever...\n")

        relevant_messages = (
            await relevant_message_retriever.retrieve(
                conversation_id=conversation_id,
                query=current_message,
                limit=3,
            )
        )

        print("\n========== RELEVANT MESSAGES ==========\n")

        print(
            f"Number of relevant messages: "
            f"{len(relevant_messages)}"
        )

        for result in relevant_messages:

            print(
                f"score={result.relevance_score:.2f} | "
                f"source={result.retrieval_source} | "
                f"role={result.message.role} | "
                f"sequence={result.message.sequence_number}"
            )

            print(
                f"content={result.message.content}\n"
            )

        print("========================================\n")

        # -----------------------------------------------------
        # Test ContextManager
        # -----------------------------------------------------

        print("Calling ContextManager...\n")

        context = await context_manager.build_context(
            conversation_id=conversation_id,
            history=messages,
            current_message=current_message,
        )

        # -----------------------------------------------------
        # Final Context
        # -----------------------------------------------------

        print("\n========== FINAL CONTEXT ==========\n")

        print(context)

        print("\n===================================\n")


if __name__ == "__main__":
    asyncio.run(main())