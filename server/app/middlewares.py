import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.settings import settings

log = structlog.get_logger()


def add_cors_middleware(app: FastAPI) -> None:
    allowed_origins = settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS else []
    allowed_origins.append(settings.WEB_BASE_URL)
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


def add_logfire_middleware(app: FastAPI) -> None:
    from app._logfire import LogfireClientTracesMiddleware

    app.add_middleware(LogfireClientTracesMiddleware)


def setup_middlewares(app: FastAPI) -> None:
    add_cors_middleware(app)
    add_session_middleware(app)
    add_logfire_middleware(app)
