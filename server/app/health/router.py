from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app import __version__
from app.health.schemas import ReadinessCheck
from app.kit.postgres import AsyncSession, get_async_db_session
from app.kit.utils import utc_now

router = APIRouter(tags=["health"])


@router.get("/livez", response_class=Response)
async def liveliness_check() -> Response:
    return Response(status_code=status.HTTP_200_OK)


@router.get("/readyz", response_model=ReadinessCheck)
async def readiness_check(
    _: AsyncSession = Depends(get_async_db_session),
) -> ReadinessCheck:
    return ReadinessCheck(message="All systems go.", version=__version__, t=utc_now())


@router.get("/failz", response_class=Response)
async def failz(how: str = Query("http")) -> Response:
    if how == "http":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="http-🔥"
        )
    else:
        raise Exception("exc-🔥")
