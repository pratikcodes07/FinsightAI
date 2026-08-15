from __future__ import annotations

from fastapi import APIRouter

from finsight_ai.api.v1.endpoints.auth import router as auth_router
from finsight_ai.api.v1.endpoints.health import router as health_router

router = APIRouter()
router.include_router(health_router, tags=["health"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
