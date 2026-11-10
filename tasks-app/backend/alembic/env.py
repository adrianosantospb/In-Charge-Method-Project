"""Alembic environment: runs migrations against TASKS_DATABASE_URL."""

from alembic import context
from sqlmodel import SQLModel

from app import models  # noqa: F401  (registers the tables)
from app.db import get_engine

target_metadata = SQLModel.metadata


def run_migrations() -> None:
    with get_engine().connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    raise SystemExit("Offline migrations are not supported. Run against a database.")
run_migrations()
