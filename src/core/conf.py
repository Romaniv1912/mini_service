import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings

from src.common.settings import AppSettings, DatabaseSettings

# Get the project root directory
# Or use an absolute path to the backend directory
BASE_PATH = Path(__file__).resolve().parent.parent.parent

# Log file path
LOG_DIR = os.path.join(BASE_PATH, 'logs')


class Settings(BaseSettings):
    """Global Settings"""

    # Env Config
    ENVIRONMENT: Literal['dev', 'pro']

    APP: AppSettings = AppSettings()


@lru_cache
def get_settings() -> Settings:
    """Get global configuration"""
    return AppSettings()


# Create configuration instance
settings = get_settings()