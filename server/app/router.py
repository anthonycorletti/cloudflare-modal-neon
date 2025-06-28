from fastapi import APIRouter

from app._logfire import router as metrics_router
from app.health.router import router as health_router
from app.items.router import router as items_router

router = APIRouter()

# /health
router.include_router(health_router)

# /items
router.include_router(items_router)

# /metrics
router.include_router(metrics_router)
