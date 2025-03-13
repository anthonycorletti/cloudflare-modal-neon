from fastapi import APIRouter, Response, status

from app import __version__
from app.health.schemas import ReadinessCheck
from app.kit.utils import utc_now

router = APIRouter(tags=["health"])


@router.get("/livez", response_class=Response)
async def liveliness_check() -> Response:
    return Response(status_code=status.HTTP_200_OK)


@router.get("/readyz", response_model=ReadinessCheck)
async def readiness_check() -> ReadinessCheck:
    return ReadinessCheck(message="All systems go.", version=__version__, t=utc_now())
