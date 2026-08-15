from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from finsight_ai.schemas.auth import AuthLoginRequest, AuthTokenPair, AuthRefreshRequest

router = APIRouter()


@router.post("/login", response_model=AuthTokenPair, summary="Authenticate a user")
async def login(_: AuthLoginRequest) -> AuthTokenPair:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication flow will be enabled after the identity tables and seed strategy are finalized.",
    )


@router.post("/refresh", response_model=AuthTokenPair, summary="Refresh an access token")
async def refresh(_: AuthRefreshRequest) -> AuthTokenPair:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Token refresh will be enabled after the auth service and persistence layer are implemented.",
    )
