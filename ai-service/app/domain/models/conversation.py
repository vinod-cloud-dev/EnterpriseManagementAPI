from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class Conversation:
    id: UUID
    user_id: int
    user_email: str
    title: str | None
    created_at: datetime
    updated_at: datetime
    last_message_at: datetime
    is_archived: bool