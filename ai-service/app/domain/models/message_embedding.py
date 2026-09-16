from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class MessageEmbedding:
    id: UUID
    message_id: UUID
    conversation_id: UUID
    embedding: list[float]
    model_name: str
    created_at: datetime
    updated_at: datetime