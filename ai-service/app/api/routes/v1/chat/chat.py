from fastapi import APIRouter, Depends
from app.api.dependencies.conversation import get_conversation_service
from app.application.services.conversation_service import ConversationService
from app.domain.models.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest,conversation_service: ConversationService = Depends(get_conversation_service),
) -> ChatResponse:
    response = await conversation_service.chat(conversation_id=request.conversation_id,message=request.message,)
    return ChatResponse(response=response)