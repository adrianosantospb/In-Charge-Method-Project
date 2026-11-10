"""Settings read from environment variables. Nothing secret has a default."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TASKS_", extra="ignore")

    database_url: str
    # Signs the session tokens. At least 32 characters; generate it, never type it.
    jwt_secret: str = Field(min_length=32)
    access_token_minutes: int = Field(default=30, ge=1, le=24 * 60)
    # Browsers send a Secure cookie only over HTTPS. Turn it off only for local HTTP.
    cookie_secure: bool = True
    # The interactive API documentation at /api/docs. Off unless turned on.
    api_docs: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
