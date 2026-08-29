from uuid import UUID, uuid4
from app.application.interfaces.conversation_memory import (ConversationMemoryInterface,)
from app.application.interfaces.llm import LLMInterface
from app.domain.models.conversation_message import ConversationMessage 
from app.application.interfaces.context_builder import (ContextBuilderInterface,)
from datetime import datetime, timezone

class ConversationService:

    def __init__(
        self,
        llm: LLMInterface,
        memory: ConversationMemoryInterface,
        context_builder: ContextBuilderInterface,
    ) -> None:
        self._llm = llm
        self._memory = memory
        self._context_builder = context_builder

    async def chat(
        self,
        conversation_id: UUID,
        message: str,
    ) -> str:

        history = await self._memory.get_history(
            conversation_id
        )

        prompt = self._context_builder.build(
            history,
            message,
        )

        response = await self._llm.generate(prompt)

        next_sequence = len(history) + 1

        await self._memory.add_message(
            ConversationMessage(
                id=uuid4(),
                conversation_id=conversation_id,
                role="user",
                content=message,
                created_at=datetime.now(timezone.utc),
                sequence_number=next_sequence,
            )
        )

        await self._memory.add_message(
            ConversationMessage(
                id=uuid4(),
                conversation_id=conversation_id,
                role="assistant",
                content=response,
                created_at=datetime.now(timezone.utc),
                sequence_number=next_sequence + 1,
            )
        )

        return response