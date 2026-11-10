"""Sign up, sign in and sign out, including the denied paths."""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
from fastapi.testclient import TestClient

from app.security import ALGORITHM, COOKIE_NAME
from tests.conftest import JSON, PASSWORD, sign_up


def test_register_signs_the_user_in(client: TestClient) -> None:
    response = client.post(
        "/api/auth/register", json={"email": "Alice@Example.com ", "password": PASSWORD}
    )

    assert response.status_code == 201
    assert response.json()["email"] == "alice@example.com"
    assert "password" not in response.text
    assert client.get("/api/auth/me").status_code == 200


def test_session_cookie_is_http_only_and_strict(client: TestClient) -> None:
    response = client.post(
        "/api/auth/register", json={"email": "alice@example.com", "password": PASSWORD}
    )

    cookie = response.headers["set-cookie"].lower()
    assert "httponly" in cookie
    assert "samesite=strict" in cookie
    assert "path=/api" in cookie


def test_register_twice_with_the_same_email_is_rejected(client: TestClient) -> None:
    sign_up(client, "alice@example.com")

    response = client.post(
        "/api/auth/register", json={"email": "ALICE@example.com", "password": PASSWORD}
    )

    assert response.status_code == 409


def test_short_password_is_rejected(client: TestClient) -> None:
    response = client.post(
        "/api/auth/register", json={"email": "alice@example.com", "password": "short"}
    )

    assert response.status_code == 422


def test_login_with_the_right_password(client: TestClient) -> None:
    sign_up(client, "alice@example.com")
    client.cookies.clear()

    response = client.post(
        "/api/auth/login", json={"email": "alice@example.com", "password": PASSWORD}
    )

    assert response.status_code == 200
    assert client.get("/api/auth/me").json()["email"] == "alice@example.com"


def test_wrong_password_and_unknown_email_get_the_same_answer(client: TestClient) -> None:
    sign_up(client, "alice@example.com")
    client.cookies.clear()

    wrong_password = client.post(
        "/api/auth/login", json={"email": "alice@example.com", "password": "not the password"}
    )
    unknown_email = client.post(
        "/api/auth/login", json={"email": "nobody@example.com", "password": PASSWORD}
    )

    assert wrong_password.status_code == unknown_email.status_code == 401
    assert wrong_password.json() == unknown_email.json()
    assert COOKIE_NAME not in client.cookies


def test_logout_ends_the_session(alice: TestClient) -> None:
    assert alice.post("/api/auth/logout").status_code == 204

    assert alice.get("/api/auth/me").status_code == 401


def test_me_without_a_session_is_denied(client: TestClient) -> None:
    assert client.get("/api/auth/me").status_code == 401


def test_tampered_token_is_denied(alice: TestClient) -> None:
    token = alice.cookies[COOKIE_NAME]
    alice.cookies.set(COOKIE_NAME, token[:-2] + ("AA" if token[-2:] != "AA" else "BB"), path="/api")

    assert alice.get("/api/auth/me").status_code == 401


def test_token_signed_with_another_secret_is_denied(client: TestClient) -> None:
    sign_up(client, "alice@example.com")
    now = datetime.now(UTC)
    forged = jwt.encode(
        {"sub": str(uuid4()), "iat": now, "exp": now + timedelta(minutes=5)},
        "another-secret-that-is-long-enough-to-sign",
        algorithm=ALGORITHM,
    )
    client.cookies.set(COOKIE_NAME, forged, path="/api")

    assert client.get("/api/auth/me").status_code == 401


def test_expired_token_is_denied(client: TestClient) -> None:
    from app.config import get_settings

    user_id = sign_up(client, "alice@example.com").get("/api/auth/me").json()["id"]
    past = datetime.now(UTC) - timedelta(hours=2)
    expired = jwt.encode(
        {"sub": user_id, "iat": past, "exp": past + timedelta(minutes=30)},
        get_settings().jwt_secret,
        algorithm=ALGORITHM,
    )
    client.cookies.set(COOKIE_NAME, expired, path="/api")

    assert client.get("/api/auth/me").status_code == 401


def test_token_for_a_user_that_does_not_exist_is_denied(client: TestClient) -> None:
    from app.config import get_settings

    now = datetime.now(UTC)
    token = jwt.encode(
        {"sub": str(uuid4()), "iat": now, "exp": now + timedelta(minutes=5)},
        get_settings().jwt_secret,
        algorithm=ALGORITHM,
    )
    client.cookies.set(COOKIE_NAME, token, path="/api")

    assert client.get("/api/auth/me").status_code == 401


def test_unsigned_token_is_denied(client: TestClient) -> None:
    user_id = sign_up(client, "alice@example.com").get("/api/auth/me").json()["id"]
    unsigned = jwt.encode({"sub": user_id}, key=None, algorithm="none")
    client.cookies.set(COOKIE_NAME, unsigned, path="/api")

    assert client.get("/api/auth/me").status_code == 401


def test_cookie_is_secure_unless_turned_off(monkeypatch) -> None:
    from app.config import get_settings
    from app.main import create_app

    monkeypatch.setenv("TASKS_COOKIE_SECURE", "true")
    get_settings.cache_clear()
    try:
        with TestClient(create_app(), headers=JSON) as client:
            response = client.post(
                "/api/auth/register", json={"email": "alice@example.com", "password": PASSWORD}
            )
        assert "secure" in response.headers["set-cookie"].lower()
    finally:
        get_settings.cache_clear()


def test_changes_without_json_content_type_are_refused(alice: TestClient) -> None:
    form = alice.post("/api/tasks", content="title=x", headers={"Content-Type": "text/plain"})
    no_type = alice.request("POST", "/api/auth/logout", headers={"Content-Type": ""})

    assert form.status_code == no_type.status_code == 415
    assert alice.get("/api/auth/me").status_code == 200


def test_api_docs_are_off_by_default(client: TestClient) -> None:
    assert client.get("/api/docs").status_code == 404
    assert client.get("/api/openapi.json").status_code == 404


def test_json_with_a_charset_is_accepted(alice: TestClient) -> None:
    response = alice.post(
        "/api/tasks",
        content='{"title": "Buy milk"}',
        headers={"Content-Type": "Application/JSON; charset=utf-8"},
    )

    assert response.status_code == 201
