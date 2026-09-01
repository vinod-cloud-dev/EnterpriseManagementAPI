from fastapi import APIRouter

from app.api.routes.v1.chat.chat import router as chat_router
from app.api.routes.v1.health import router as health_router

router = APIRouter()
router.include_router(health_router, tags=["health"], prefix="/health")
router.include_router(chat_router, prefix="/ai",tags=["ai"],)