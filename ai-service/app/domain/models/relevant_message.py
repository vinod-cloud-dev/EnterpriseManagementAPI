from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RelevantMessage:
    message_id: UUID
    conversation_id: UUID
    content: str
    role: str
    similarity_score: float