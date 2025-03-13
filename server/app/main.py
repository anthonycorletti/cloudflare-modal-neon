import os
from contextlib import asynccontextmanager
from typing import AsyncIterator, TypedDict

import structlog
from fastapi import Depends, FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.routing import APIRoute

from app import __version__
from app.kit.postgres import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    create_async_sessionmaker,
    get_async_db_session,
)
from app.logging import configure_logging
from app.middlewares import setup_middlewares
from app.router import router
from app.settings import settings

log = structlog.get_logger()

os.environ["TZ"] = "UTC"


def generate_unique_openapi_id(route: APIRoute) -> str:
    return f"{route.tags[0]}:{route.name}"


class State(TypedDict):
    asyncengine: AsyncEngine
    asyncsessionmaker: async_sessionmaker[AsyncSession]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    log.info("starting up app services...")
    asyncengine = create_async_engine("app")
    asyncsessionmaker = create_async_sessionmaker(asyncengine)
    log.info("app started")
    yield {"asyncengine": asyncengine, "asyncsessionmaker": asyncsessionmaker}
    await asyncengine.dispose()
    log.info("app stopped")


def create_app() -> FastAPI:
    app = FastAPI(
        title=f"Feature Money Server API ({settings.SERVER_API_BASE_URL})",
        generate_unique_id_function=generate_unique_openapi_id,
        version=__version__,
        lifespan=lifespan,
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    @app.get("/docs", tags=["docs"])
    async def get_documentation(
        request: Request, session: AsyncSession = Depends(get_async_db_session)
    ) -> HTMLResponse:
        # current_user_admin = await AuthService().current_user_admin(
        #     request=request, session=session
        # )
        # if current_user_admin is None:
        #     raise HTTPException(status_code=404)
        return get_swagger_ui_html(openapi_url="/openapi.json", title=app.title)

    @app.get("/openapi.json", tags=["docs"])
    async def openapi(
        request: Request, session: AsyncSession = Depends(get_async_db_session)
    ) -> JSONResponse:
        # current_user_admin = await AuthService().current_user_admin(
        #     request=request, session=session
        # )
        # if current_user_admin is None:
        #     raise HTTPException(status_code=404)
        return JSONResponse(
            get_openapi(title=app.title, version=app.version, routes=app.routes)
        )

    setup_middlewares(app)
    app.include_router(router)

    return app


configure_logging()

app = create_app()
