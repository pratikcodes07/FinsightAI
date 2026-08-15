# FinSight AI Backend

Backend foundation for FinSight AI, built with a `src/` layout and designed to stay modular as the product grows.

## What is in scope now

- Phase 0: backend architecture, settings, packaging, logging, env templates, and project conventions
- Phase 1: database foundation, auth scaffolding, API versioning, health checks, Celery wiring, and Alembic migration setup

## Proposed backend layout

- `src/finsight_ai/app.py` - application factory
- `src/finsight_ai/api/` - versioned API routers and dependencies
- `src/finsight_ai/core/` - settings, logging, security, and shared error types
- `src/finsight_ai/db/` - database engine and session management
- `src/finsight_ai/models/` - SQLAlchemy models
- `src/finsight_ai/schemas/` - Pydantic request and response models
- `src/finsight_ai/services/` - business logic
- `src/finsight_ai/repositories/` - persistence access layer
- `src/finsight_ai/workers/` - Celery app and async jobs
- `alembic/` - database migration environment

## Next steps after the scaffold

1. Wire the database connection and first migrations.
2. Add user/auth persistence and token issuance.
3. Add document metadata tables and upload pipeline contracts.
4. Layer in ingestion, retrieval, and analytics services.
