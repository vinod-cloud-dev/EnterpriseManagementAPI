from uuid import UUID
from app.application.interfaces.conversation_memory import (
    ConversationMemoryInterface,
)
from app.application.interfaces.llm import LLMInterface
from app.domain.models.conversation_message import ConversationMessage


class ConversationService:

    def __init__(
        self,
        llm: LLMInterface,
        memory: ConversationMemoryInterface,
    ) -> None:
        self._llm = llm
        self._memory = memory

    async def chat(
        self,
        conversation_id: UUID,
        message: str,
    ) -> str:

        history = await self._memory.get_history(
            conversation_id
        )

        prompt = self._build_prompt(
            history,
            message,
        )

        response = await self._llm.generate(prompt)

        await self._memory.add_message(
            ConversationMessage(
                conversation_id=conversation_id,
                role="user",
                content=message,
                created_at=__import__("datetime").datetime.utcnow(),
            )
        )

        await self._memory.add_message(
            ConversationMessage(
                conversation_id=conversation_id,
                role="assistant",
                content=response,
                created_at=__import__("datetime").datetime.utcnow(),
            )
        )

        return response

    @staticmethod
    def _build_prompt(
        history: list[ConversationMessage],
        current_message: str,
    ) -> str:

        conversation = "\n".join(
            f"{message.role}: {message.content}"
            for message in history
        )

        return (
            f"{conversation}\n"
            f"user: {current_message}\n"
            f"assistant:"
        )