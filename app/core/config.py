from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Todo AI Agent"

    # Database Configuration
    DATABASE_URL: str

    # OpenRouter/LLM Configuration
    OPENROUTER_API_KEY: str
    OPENROUTER_MODEL: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()

