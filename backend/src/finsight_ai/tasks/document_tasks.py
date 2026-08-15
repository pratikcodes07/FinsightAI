from __future__ import annotations

from celery import shared_task


@shared_task(name="finsight_ai.documents.extract_metadata")
def extract_document_metadata(document_id: str) -> dict[str, str]:
    return {
        "document_id": document_id,
        "status": "queued",
    }
