from pydantic_settings import SettingsConfigDict, BaseSettings


class AppSettings(BaseSettings):
    """App Settings"""

    model_config = SettingsConfigDict(env_prefix='APP_')

    # FastAPI
    TITLE: str
    VERSION: str
    DESCRIPTION: str
    DOCS_URL: str | None = None
    REDOCS_URL: str | None = None
    OPENAPI_URL: str | None = None
    BASE_PATH: str

    DB_URL: str
