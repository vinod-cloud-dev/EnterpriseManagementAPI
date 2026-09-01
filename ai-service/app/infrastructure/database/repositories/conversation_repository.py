from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.application.interfaces.conversation_repository import (
    ConversationRepositoryInterface,
)
from app.domain.models.conversation_message import (
    ConversationMessage as DomainConversationMessage,
)
from app.infrastructure.database.models.conversation_message import (
    ConversationMessage as ConversationMessageModel,
)
from app.infrastructure.database.models.conversation import Conversation

class ConversationRepository(ConversationRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    async def save_message(
        self,
        message: DomainConversationMessage,
    ) -> None:

        db_message = ConversationMessageModel(
            id=message.id,
            conversation_id=message.conversation_id,
            role=message.role,
            content=message.content,
            created_at=message.created_at,
            sequence_number=message.sequence_number,
        )

        self._session.add(db_message)

        # Update conversation timestamps
        conversation = await self._session.get(
            Conversation,
            message.conversation_id,
        )

        if conversation is not None:
            conversation.updated_at = message.created_at
            conversation.last_message_at = message.created_at

        await self._session.commit()
    async def get_history(
        self,
        conversation_id: UUID,
    ) -> list[DomainConversationMessage]:

        result = await self._session.execute(
            select(ConversationMessageModel)
            .where(
                ConversationMessageModel.conversation_id
                == conversation_id
            )
            .order_by(
                ConversationMessageModel.sequence_number
            )
        )

        db_messages = result.scalars().all()

        return [
            DomainConversationMessage(
                id=db_message.id,
                conversation_id=db_message.conversation_id,
                role=db_message.role,
                content=db_message.content,
                created_at=db_message.created_at,
                sequence_number=db_message.sequence_number,
            )
            for db_message in db_messages
        ]

    async def create_conversation(
        self,
        conversation_id: UUID,
        user_id: int,
    ) -> None:

        now = datetime.now(timezone.utc)
        conversation = Conversation(
            id=conversation_id,
            user_id=user_id,
            created_at=now,
            updated_at=now,
            last_message_at=now,
            is_archived=False,
        )
        self._session.add(conversation)
        await self._session.commit()

    async def get_conversation(
        self,
        conversation_id: UUID,
        user_id: int,
    ) -> bool:
        result = await self._session.execute(
            select(Conversation.id)
            .where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
        )

        return result.scalar_one_or_none() is not None
    
    
    
    
    async def get_conversation_owner(
        self,
        conversation_id: UUID,
         ) -> int | None:
        result = await self._session.execute(
            select(Conversation.user_id)
            .where(
                Conversation.id == conversation_id
            )
        )
        return result.scalar_one_or_none()