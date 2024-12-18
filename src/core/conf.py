import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings

from src.common.settings import AppSettings, LogSettings

# Get the project root directory
# Or use an absolute path to the backend directory
BASE_PATH = Path(__file__).resolve().parent.parent.parent

# Log file path
LOG_DIR = os.path.join(BASE_PATH, "logs")


class Settings(BaseSettings):
    """Global Settings"""

    APP: AppSettings = AppSettings()
    LOG: LogSettings = LogSettings()


@lru_cache
def get_settings() -> Settings:
    """Get global configuration"""
    return Settings()


# Create configuration instance
settings = get_settings()
