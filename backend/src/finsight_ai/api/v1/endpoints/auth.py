from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from finsight_ai.api.deps import SettingsDep, get_db_session
from finsight_ai.core.config import Settings
from finsight_ai.core.errors import ConflictError
from finsight_ai.schemas.auth import AuthLoginRequest, AuthRefreshRequest, AuthTokenPair
from finsight_ai.schemas.user import UserCreate
from finsight_ai.services.auth import AuthService

router = APIRouter()


@router.post(
    "/signup",
    response_model=AuthTokenPair,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user and issue JWTs",
)
async def signup(
    payload: UserCreate,
    session: AsyncSession = Depends(get_db_session),
    settings: Settings = SettingsDep,
) -> AuthTokenPair:
    service = AuthService(session, settings)
    try:
        return await service.signup(payload)
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.post("/login", response_model=AuthTokenPair, summary="Authenticate a user")
async def login(
    payload: AuthLoginRequest,
    session: AsyncSession = Depends(get_db_session),
    settings: Settings = SettingsDep,
) -> AuthTokenPair:
    service = AuthService(session, settings)
    token_pair = await service.authenticate(payload)
    if token_pair is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return token_pair


@router.post("/refresh", response_model=AuthTokenPair, summary="Refresh an access token")
async def refresh(_: AuthRefreshRequest) -> AuthTokenPair:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Token refresh will be enabled after the auth service and persistence layer are implemented.",
    )
