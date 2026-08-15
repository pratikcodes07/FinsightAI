from __future__ import annotations

from fastapi import APIRouter

from finsight_ai import __version__
from finsight_ai.schemas.health import HealthResponse

router = APIRouter(prefix="/health")


@router.get("", response_model=HealthResponse, summary="Health check")
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", service="finsight-ai", version=__version__)


@router.get("/ready", response_model=HealthResponse, summary="Readiness check")
async def readiness_check() -> HealthResponse:
    return HealthResponse(status="ready", service="finsight-ai", version=__version__)
