from __future__ import annotations

from celery import Celery

from finsight_ai.core.config import get_settings


def create_celery_app() -> Celery:
    settings = get_settings()
    app = Celery(
        "finsight_ai",
        broker=settings.celery_broker_url,
        backend=settings.celery_result_backend,
        include=["finsight_ai.tasks.document_tasks"],
    )
    app.conf.update(
        task_track_started=True,
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        enable_utc=True,
    )
    return app


celery_app = create_celery_app()
