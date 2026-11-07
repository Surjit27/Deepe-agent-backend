from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    env: str = "development"
    port: int = 4100
    log_level: str = "info"
    internal_api_key: str = "dev-internal-key-change-me"

    database_url: str = "postgresql+psycopg://aazhi:aazhi@127.0.0.1:5433/aazhi"
    postgres_schema: str = "ai"

    mongodb_uri: str = "mongodb://127.0.0.1:27017/aazhi"
    repo_workdir: str = "/tmp/aazhi-repos"

    openai_api_key: str = ""
    google_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
