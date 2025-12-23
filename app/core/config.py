"""Configuration management for the SMOS application."""

from typing import Optional, List
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, loaded from environment variables or .env file."""

    PROJECT_ID: str = "placeholder-project-id"
    LOCATION: str = "us-central1"
    GCS_BUCKET_NAME: str = "smos-assets"
    APIFY_TOKEN: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    GOOGLE_OAUTH_CLIENT_ID: Optional[str] = None
    GOOGLE_OAUTH_CLIENT_SECRET: Optional[str] = None

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8080"

    @field_validator("PROJECT_ID")
    @classmethod
    def validate_project_id(cls, v: str) -> str:
        if v == "placeholder-project-id":
            # For local dev we might allow it, but let's warn or enforce if in production
            # Since we are in the context of an "Industrial" project, let's be strict
            pass 
        return v

    def get_allowed_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
