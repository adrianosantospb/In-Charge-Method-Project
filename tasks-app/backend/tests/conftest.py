"""Test setup: a real PostgreSQL database, migrated once, emptied before each test."""

import os
from collections.abc import Iterator

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.engine import make_url

os.environ.setdefault("TASKS_JWT_SECRET", "test-secret-that-is-long-enough-for-hs256")
os.environ.setdefault("TASKS_COOKIE_SECURE", "false")


TEST_DATABASE_RULE = (
    "The tests empty every table. Point TASKS_DATABASE_URL at a database whose name ends in _test."
)


def is_test_name(name: str | None) -> bool:
    return (name or "").endswith("_test")


def is_test_database(url: str) -> bool:
    """The tests empty every table, so they only run on a database whose name ends in _test."""
    return is_test_name(make_url(url).database)


if "TASKS_DATABASE_URL" not in os.environ:
    raise RuntimeError("Set TASKS_DATABASE_URL to an empty test database.")
if not is_test_database(os.environ["TASKS_DATABASE_URL"]):
    raise RuntimeError(TEST_DATABASE_RULE)

from app.db import get_engine  # noqa: E402
from app.main import create_app  # noqa: E402

PASSWORD = "correct horse battery"
# The webapp sends this header on every request; the API refuses changes without it.
JSON = {"Content-Type": "application/json"}


@pytest.fixture(scope="session", autouse=True)
def migrated_database() -> None:
    # The URL can name one database and connect to another, for example with a dbname
    # query parameter, so check the database the server reports too.
    with get_engine().connect() as connection:
        if not is_test_name(connection.execute(text("SELECT current_database()")).scalar()):
            raise RuntimeError(TEST_DATABASE_RULE)
    command.upgrade(Config("alembic.ini"), "head")


@pytest.fixture(autouse=True)
def empty_tables() -> None:
    with get_engine().begin() as connection:
        connection.execute(text("TRUNCATE tasks, users CASCADE"))


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(create_app(), headers=JSON) as test_client:
        yield test_client


def sign_up(client: TestClient, email: str) -> TestClient:
    response = client.post("/api/auth/register", json={"email": email, "password": PASSWORD})
    assert response.status_code == 201, response.text
    return client


@pytest.fixture
def alice(client: TestClient) -> TestClient:
    return sign_up(client, "alice@example.com")


@pytest.fixture
def bob() -> Iterator[TestClient]:
    with TestClient(create_app(), headers=JSON) as other:
        yield sign_up(other, "bob@example.com")
