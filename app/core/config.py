"""Configuration management for the SMOS application."""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, loaded from environment variables or .env file."""

    PROJECT_ID: str = "placeholder-project-id"
    LOCATION: str = "us-central1"
    GCS_BUCKET_NAME: str = "smos-assets"
    APIFY_TOKEN: Optional[str] = None

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
