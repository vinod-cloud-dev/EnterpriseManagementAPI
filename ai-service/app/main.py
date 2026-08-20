from fastapi import FastAPI

from app.api.middleware.exception_handlers import register_exception_handlers
from app.api.middleware.request_id import RequestIDMiddleware
from app.api.routes.router import api_router
from app.core.config.settings import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name, version=settings.app_version)
app.add_middleware(RequestIDMiddleware)
app.include_router(api_router)
register_exception_handlers(app)


@app.get("/")
async def root():
    return {"message": "Employee AI Service is running"}
