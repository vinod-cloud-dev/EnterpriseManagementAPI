from dataclasses import dataclass
from app.domain.models.conversation_message import ConversationMessage

@dataclass
class RetrievedMessage:
    message: ConversationMessage
    relevance_score: float
    retrieval_source: str