from typing import Any, Callable, cast

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.types import ASGIApp

from app.settings import settings

log = structlog.get_logger()


def _middleware_factory(
    middleware_class: CORSMiddleware | SessionMiddleware | Any,
) -> Any:
    return cast(Callable[[ASGIApp], ASGIApp], middleware_class)


def add_cors_middleware(app: FastAPI) -> None:
    allowed_origins = settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS else []
    allowed_origins.append(settings.WEB_BASE_URL)
    return (
        None
        if not allowed_origins
        else app.add_middleware(
            _middleware_factory(CORSMiddleware),
            allow_origins=allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    )


def add_session_middleware(app: FastAPI) -> None:
    app.add_middleware(
        _middleware_factory(SessionMiddleware), secret_key=settings.SECRET_KEY
    )


def add_logfire_middleware(app: FastAPI) -> None:
    from app._logfire import LogfireClientTracesMiddleware

    app.add_middleware(_middleware_factory(LogfireClientTracesMiddleware))


def setup_middlewares(app: FastAPI) -> None:
    add_cors_middleware(app)
    add_session_middleware(app)
    add_logfire_middleware(app)
