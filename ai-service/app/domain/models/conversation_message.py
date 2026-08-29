from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class ConversationMessage:
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    created_at: datetime
    sequence_number: int