from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from finsight_ai.core.config import Settings
from finsight_ai.core.security import create_access_token, hash_password, verify_password
from finsight_ai.models.user import User
from finsight_ai.repositories.user_repository import UserRepository
from finsight_ai.schemas.auth import AuthLoginRequest, AuthTokenPair
from finsight_ai.schemas.user import UserCreate


class AuthService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.users = UserRepository(session)

    async def register_user(self, payload: UserCreate) -> User:
        user = User(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=hash_password(payload.password),
        )
        await self.users.add(user)
        await self.session.commit()
        return user

    async def authenticate(self, payload: AuthLoginRequest) -> AuthTokenPair | None:
        user = await self.users.get_by_email(payload.email)
        if user is None or not verify_password(payload.password, user.hashed_password):
            return None

        access_token = create_access_token(str(user.id), self.settings)
        refresh_token = self._create_refresh_token(str(user.id))
        return AuthTokenPair(access_token=access_token, refresh_token=refresh_token)

    def _create_refresh_token(self, subject: str) -> str:
        now = datetime.now(tz=UTC)
        expires_at = now + timedelta(days=self.settings.refresh_token_expire_days)
        payload = {
            "sub": subject,
            "iat": int(now.timestamp()),
            "exp": int(expires_at.timestamp()),
            "type": "refresh",
        }
        from jose import jwt

        return jwt.encode(payload, self.settings.secret_key, algorithm="HS256")
