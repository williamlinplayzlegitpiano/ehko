from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    env: str = "dev"
    log_level: str = "INFO"

    finnhub_token: Optional[str] = None
    newsapi_key: Optional[str] = None

    reddit_client_id: Optional[str] = None
    reddit_client_secret: Optional[str] = None
    reddit_user_agent: str = "ehko/0.2 by your_name"

    cache_ttl_seconds: int = 90

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
