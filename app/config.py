from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.local", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    secret_key: str = "dev-secret-change-in-production"
    database_url: str = "postgresql://appuser:change_me_strong@db:5432/appdb"
    redis_url: str = "redis://redis:6379/0"
    openai_api_key: Optional[str] = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
