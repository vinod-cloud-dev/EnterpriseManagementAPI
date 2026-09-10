
import asyncio
from uuid import uuid4
from datetime import datetime, timezone

from app.api.dependencies.llm import get_llm
from app.application.services.conversation_summarizer import ConversationSummarizer
from app.domain.models.conversation_message import ConversationMessage


async def main():

    # Create the LLM directly.
    # We are not using FastAPI Depends() here because this is
    # a standalone Python test.
    llm = get_llm()

    # Create the summarizer with the real LLM
    summarizer = ConversationSummarizer(llm)

    conversation_id = uuid4()

    messages = [
        ConversationMessage(
            id=uuid4(),
            conversation_id=conversation_id,
            role="user",
            content=(
                "My name is Vinod and I am building an Employee AI "
                "platform using FastAPI, PostgreSQL, Redis, Ollama "
                "and a local LLM."
            ),
            created_at=datetime.now(timezone.utc),
            sequence_number=1,
        ),
        ConversationMessage(
            id=uuid4(),
            conversation_id=conversation_id,
            role="assistant",
            content=(
                "That is a good architecture. FastAPI can handle "
                "the AI service while PostgreSQL can be used for "
                "persistent storage."
            ),
            created_at=datetime.now(timezone.utc),
            sequence_number=2,
        ),
        ConversationMessage(
            id=uuid4(),
            conversation_id=conversation_id,
            role="user",
            content=(
                "I want PostgreSQL to be the source of truth and "
                "Redis to be used as a fast conversation cache."
            ),
            created_at=datetime.now(timezone.utc),
            sequence_number=3,
        ),
        ConversationMessage(
            id=uuid4(),
            conversation_id=conversation_id,
            role="assistant",
            content=(
                "That approach allows PostgreSQL to provide durable "
                "conversation storage while Redis improves retrieval "
                "performance."
            ),
            created_at=datetime.now(timezone.utc),
            sequence_number=4,
        ),
        ConversationMessage(
            id=uuid4(),
            conversation_id=conversation_id,
            role="user",
            content=(
                "I also want the architecture to support conversation "
                "summarization, RAG, embeddings, agents and tools later."
            ),
            created_at=datetime.now(timezone.utc),
            sequence_number=5,
        ),
    ]

    print("Calling summarizer...\n")

    summary = await summarizer.summarize(
        existing_summary=None,
        messages=messages,
    )

    print("\n========== SUMMARY ==========")
    print(summary)
    print("==============================\n")


if __name__ == "__main__":
    asyncio.run(main())
