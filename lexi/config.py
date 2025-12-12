from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    openai_api_key: str | None = Field(default=None, env="OPENAI_API_KEY")
    redis_url: str | None = Field(default=None, env="REDIS_URL")
    database_url: str | None = Field(default=None, env="DATABASE_URL")
    newsapi_key: str | None = Field(default=None, env="NEWSAPI_KEY")
    default_country: str = Field(default="us")

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
