import json
from datetime import datetime
from uuid import UUID
from app.application.interfaces.conversation_memory import (ConversationMemoryInterface,)
from app.domain.models.conversation_message import ConversationMessage
from app.infrastructure.redis.redis_client import redis_client  

class RedisConversationMemory(ConversationMemoryInterface):
    
    # Redis cache configuration
    TTL_SECONDS = 60 * 60 * 24  # 24 hours
    MAX_HISTORY_MESSAGES = 50
    
    async def get_history(
        self,
        conversation_id: UUID,
    ) -> list[ConversationMessage]:

        key = f"ai:conversation:{conversation_id}"

        try:
            # Get only the latest 50 messages
            messages = await redis_client.lrange(
                key,
                -self.MAX_HISTORY_MESSAGES,
                -1,
            )

            return [
                ConversationMessage(
                    id=UUID(data["id"]),
                    conversation_id=UUID(data["conversation_id"]),
                    role=data["role"],
                    content=data["content"],
                    created_at=datetime.fromisoformat(data["created_at"]),
                    sequence_number=data["sequence_number"],
                )
                for data in (
                    json.loads(message)
                    for message in messages
                )
            ]
        except Exception:
            # Redis failure should not break the application.
            return []

    async def add_message(
        self,
        message: ConversationMessage,
    ) -> None:

        key = f"ai:conversation:{message.conversation_id}"

        data = {
            "id": str(message.id),
            "conversation_id": str(message.conversation_id),
            "role": message.role,
            "content": message.content,
            "created_at": message.created_at.isoformat(),
            "sequence_number": message.sequence_number,
        }

        try:
            await redis_client.rpush(
                key,
                json.dumps(data),
            )

            # Keep only latest 50 messages
            await redis_client.ltrim(
                key,
                -self.MAX_HISTORY_MESSAGES,
                -1,
            )

            # Refresh TTL whenever conversation is used
            await redis_client.expire(
                key,
                self.TTL_SECONDS,
            )

        except Exception:
            # Redis is a cache.
            # PostgreSQL remains the source of truth.
            pass