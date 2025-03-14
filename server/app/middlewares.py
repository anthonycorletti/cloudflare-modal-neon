import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.settings import settings

log = structlog.get_logger()


def add_cors_middleware(app: FastAPI) -> None:
    log.info("Adding CORS middleware", allow_origins=settings.CORS_ORIGINS or "None")
    allowed_origins = settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS else []
    return (
        None
        if not allowed_origins
        else app.add_middleware(
            CORSMiddleware,
            allow_origins=allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    )


def add_session_middleware(app: FastAPI) -> None:
    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


def setup_middlewares(app: FastAPI) -> None:
    add_cors_middleware(app)
    add_session_middleware(app)
