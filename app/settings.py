from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra="allow", case_sensitive=False)
    
    redis_dsn: str = Field("redis://localhost:6379")
    database_dsn: str = Field("sqlite+aiosqlite:///tasks.db")
    update_posts_interfal_in_seconds: int | float = Field(default=timedelta(minutes=10).total_seconds())


settings = Settings()
