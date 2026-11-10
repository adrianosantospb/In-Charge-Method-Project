"""Tables and the shapes the API accepts and returns."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import EmailStr, field_validator
from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(UTC)


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=254, unique=True, index=True)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=utc_now, sa_type=DateTime(timezone=True))


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    owner_id: UUID = Field(foreign_key="users.id", index=True, ondelete="CASCADE")
    title: str = Field(max_length=200)
    done: bool = Field(default=False)
    created_at: datetime = Field(default_factory=utc_now, sa_type=DateTime(timezone=True))
    updated_at: datetime = Field(default_factory=utc_now, sa_type=DateTime(timezone=True))


class Credentials(SQLModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)


class UserRead(SQLModel):
    id: UUID
    email: str


def _strip(value: object) -> object:
    """Strip titles before the length check, so "   " counts as empty."""
    return value.strip() if isinstance(value, str) else value


class TaskCreate(SQLModel):
    title: str = Field(min_length=1, max_length=200)

    _strip_title = field_validator("title", mode="before")(_strip)


class TaskUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    done: bool | None = None

    _strip_title = field_validator("title", mode="before")(_strip)


class TaskRead(SQLModel):
    id: UUID
    title: str
    done: bool
    created_at: datetime
    updated_at: datetime
