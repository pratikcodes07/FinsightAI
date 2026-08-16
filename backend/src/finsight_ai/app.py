from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from finsight_ai import __version__
from finsight_ai.api.router import api_router
from finsight_ai.core.config import get_settings
from finsight_ai.core.logging import configure_logging
from finsight_ai.db.base import create_tables
from finsight_ai.db.session import init_engine


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        # Import models so SQLAlchemy registers all mapped tables before create_all runs.
        from finsight_ai import models as _models  # noqa: F401

        engine = init_engine()
        await create_tables(engine)
        yield

    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        debug=settings.debug,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
        lifespan=lifespan,
    )

    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app
