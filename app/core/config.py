import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    RESEARCHER_ROLE: int = 2
    HUGGINGFACE_API_KEY: str | None = None

    model_config = SettingsConfigDict(env_file=str(ENV_PATH), env_file_encoding='utf-8')

def get_settings():
    print(f"🔍 Loading .env from: {ENV_PATH}")
    if not ENV_PATH.exists():
        print("⚠️  .env file not found!")
    return Settings()

settings = get_settings()