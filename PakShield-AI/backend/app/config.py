from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./pakshield.db"
    secret_key: str = "pakshield-ai-secret-key-change-in-production-2026"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    upload_dir: str = "./uploads"
    model_path: str = "./app/ml/yolo_cls.pt"
    max_upload_size: int = 10_485_760
    allowed_extensions: str = "png,jpg,jpeg"
    cors_origins_regex: str = "https?://(localhost:[0-9]+|.*\\.vercel\\.app|.*\\.onrender\\.com|.*\\.pythonanywhere\\.com|.*\\.railway\\.app)"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
