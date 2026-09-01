"""Centralized API exception handling."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.base import DomainError
from app.application.exceptions.base import ApplicationError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def handle_domain_error(
        _: Request,
        exc: DomainError,
    ) -> JSONResponse:

        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )

    @app.exception_handler(ApplicationError)
    async def handle_application_error(
        _: Request,
        exc: ApplicationError,
    ) -> JSONResponse:

        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )