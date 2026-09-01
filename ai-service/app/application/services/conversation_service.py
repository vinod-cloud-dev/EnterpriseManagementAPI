from uuid import UUID, uuid4
from app.application.interfaces.conversation_memory import (ConversationMemoryInterface,)
from app.application.interfaces.llm import LLMInterface
from app.domain.models.conversation_message import ConversationMessage 
from app.application.interfaces.context_builder import (ContextBuilderInterface,)
from datetime import datetime, timezone
from app.application.interfaces.conversation_repository import (
    ConversationRepositoryInterface,
)
# from app.application.exceptions.exceptions import (
#     ConversationAccessDeniedError,
# )
from app.application.exceptions.base import ConversationAccessDeniedError
class ConversationService:

    def __init__(
        self,
        llm: LLMInterface,
        memory: ConversationMemoryInterface,
        repository: ConversationRepositoryInterface,
        context_builder: ContextBuilderInterface,
    ) -> None:
        self._llm = llm
        self._memory = memory
        self._repository = repository
        self._context_builder = context_builder

    async def chat(
            self,
            conversation_id: UUID,
            message: str,
            user_id: int,
        ) -> str:

            # 1. Check whether conversation belongs to this user
            conversation_exists = await self._repository.get_conversation(
                conversation_id,
                user_id,
            )

            # 2. Conversation doesn't belong to this user
            if not conversation_exists:
                # Check whether conversation exists for another user
                owner_id = await self._repository.get_conversation_owner(
                    conversation_id
                )

                # Conversation exists but belongs to another user
                if owner_id is not None:
                    raise ConversationAccessDeniedError()

                # Conversation doesn't exist at all
                await self._repository.create_conversation(
                    conversation_id,
                    user_id,
                )

            # 3. Now it is safe to load history
            history = await self._memory.get_history(
                conversation_id
            )

            if not history:
                history = await self._repository.get_history(
                    conversation_id,
                )

            # 4. Load DB history into Redis
            for history_message in history:
                await self._memory.add_message(history_message)

            # 5. Build prompt
            prompt = self._context_builder.build(
                history,
                message,
            )
            
            print("\n========== PROMPT ==========")
            print(prompt)
            print("============================\n")

            # 6. Generate response
            response = await self._llm.generate(prompt)

            # 7. Save user message
            next_sequence = len(history) + 1
            
            user_message = ConversationMessage(
                id=uuid4(),
                conversation_id=conversation_id,
                role="user",
                content=message,
                created_at=datetime.now(timezone.utc),
                sequence_number=next_sequence,
            )

            await self._repository.save_message(user_message)
            await self._memory.add_message(user_message)

            # 8. Save assistant message
            assistant_message = ConversationMessage(
                id=uuid4(),
                conversation_id=conversation_id,
                role="assistant",
                content=response,
                created_at=datetime.now(timezone.utc),
                sequence_number=next_sequence + 1,
            )
            await self._repository.save_message(assistant_message)
            await self._memory.add_message(assistant_message)
            return response