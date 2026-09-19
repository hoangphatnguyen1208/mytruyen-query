from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "MyTruyen Query Service"
    API_V1_STR: str = "/api/v1"
    POSTGRES_URL: str
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"

settings = Settings()
