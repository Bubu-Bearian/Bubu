from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str | None = Field(default=None)
    redis_url: str | None = Field(default=None)
    database_url: str | None = Field(default=None)
    newsapi_key: str | None = Field(default=None)
    default_country: str = Field(default="us")

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
