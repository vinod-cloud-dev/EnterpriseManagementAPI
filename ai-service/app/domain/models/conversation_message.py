from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class ConversationMessage:
    conversation_id: UUID
    role: str
    content: str
    created_at: datetime