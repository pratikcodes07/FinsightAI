from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any
from uuid import UUID, uuid4

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from finsight_ai.app import create_app
from finsight_ai.api import deps as api_deps
from finsight_ai.services import auth as auth_service_module


class _FakeSession:
    def __init__(self) -> None:
        self.users_by_email: dict[str, Any] = {}
        self.committed = False

    async def commit(self) -> None:
        self.committed = True


class _FakeUserRepository:
    def __init__(self, session: _FakeSession) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> Any | None:
        return self.session.users_by_email.get(email)

    async def add(self, user: Any) -> Any:
        if getattr(user, "id", None) is None:
            user.id = uuid4()
        self.session.users_by_email[user.email] = user
        return user


def test_signup_creates_user_and_returns_tokens(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_session = _FakeSession()

    monkeypatch.setattr(auth_service_module, "UserRepository", _FakeUserRepository)

    async def override_session() -> AsyncIterator[_FakeSession]:
        yield fake_session

    app = create_app()
    app.dependency_overrides[api_deps.get_db_session] = override_session

    client = TestClient(app)
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "email": "new.user@example.com",
            "full_name": "New User",
            "password": "supersecret123",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"].count(".") == 2
    assert body["refresh_token"].count(".") == 2
    assert "new.user@example.com" in fake_session.users_by_email
    created_user = fake_session.users_by_email["new.user@example.com"]
    assert isinstance(created_user.id, UUID)
    assert fake_session.committed is True

    duplicate_response = client.post(
        "/api/v1/auth/signup",
        json={
            "email": "new.user@example.com",
            "full_name": "New User",
            "password": "supersecret123",
        },
    )
    assert duplicate_response.status_code == 409
