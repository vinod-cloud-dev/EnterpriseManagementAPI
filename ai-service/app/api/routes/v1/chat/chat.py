from fastapi import APIRouter, Depends
from app.api.dependencies.auth import get_current_user
from app.api.dependencies.conversation import get_conversation_service
from app.application.services.conversation_service import ConversationService
from app.domain.models.chat import ChatRequest, ChatResponse
from app.domain.models.current_user import CurrentUser

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest,conversation_service: ConversationService = Depends(get_conversation_service),
    current_user: CurrentUser = Depends(get_current_user),) -> ChatResponse:
    
    response = await conversation_service.chat(
        conversation_id=request.conversation_id,
        message=request.message,
        user_id=current_user.user_id,
    )

    return ChatResponse(response=response)