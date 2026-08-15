from __future__ import annotations

from collections.abc import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from finsight_ai.core.config import Settings, get_settings
from finsight_ai.db.session import get_session_factory


def settings_dep() -> Settings:
    return get_settings()


async def get_db_session() -> AsyncIterator[AsyncSession]:
    session_factory = get_session_factory()
    async with session_factory() as session:
        yield session


SettingsDep = Depends(settings_dep)
