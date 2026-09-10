from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class ConversationSummary:
    conversation_id: UUID
    summary: str
    summarized_until_sequence: int
    created_at: datetime
    updated_at: datetime