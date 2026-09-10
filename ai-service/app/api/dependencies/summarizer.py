from fastapi import Depends

from app.application.interfaces.conversation_summarizer import (
    ConversationSummarizerInterface,
)
from app.application.interfaces.llm import LLMInterface
from app.application.services.conversation_summarizer import (
    ConversationSummarizer,
)
from app.api.dependencies.llm import get_llm


def get_conversation_summarizer(
    llm: LLMInterface = Depends(get_llm),
) -> ConversationSummarizerInterface:
    return ConversationSummarizer(llm)