from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    APP_SECRET_KEY: str = "change-me-to-a-secure-random-key"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/scrriber.db"

    # AI Intelligence Providers
    GEMINI_API_KEY: Optional[str] = Field(default=None)
    OPENAI_API_KEY: Optional[str] = Field(default=None)

    # Cloud Storage (Optional / Phase 5)
    R2_ACCOUNT_ID: Optional[str] = None
    R2_ACCESS_KEY_ID: Optional[str] = None
    R2_SECRET_ACCESS_KEY: Optional[str] = None
    R2_BUCKET_NAME: str = "scrriber-assets"
    R2_PUBLIC_DOMAIN: Optional[str] = None

    # Meta Instagram Graph API (Phase 5)
    META_APP_ID: Optional[str] = None
    META_APP_SECRET: Optional[str] = None
    META_USER_ACCESS_TOKEN: Optional[str] = None
    INSTAGRAM_ACCOUNT_ID: Optional[str] = None

    # Base Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = Path(__file__).resolve().parent.parent.parent / "data"
    PROCESSED_ASSETS_DIR: Path = Path(__file__).resolve().parent.parent.parent / "data" / "processed_assets"

settings = Settings()
