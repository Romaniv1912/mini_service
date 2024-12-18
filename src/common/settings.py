from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """App Settings"""

    model_config = SettingsConfigDict(env_prefix='APP_')

    # FastAPI
    DEBUG: bool = False
    TITLE: str
    VERSION: str
    DESCRIPTION: str
    DOCS_URL: str | None = None
    REDOCS_URL: str | None = None
    OPENAPI_URL: str | None = None
    BASE_PATH: str

    # Database
    DB_URL: str
    DB_ECHO: bool = False

    # Trace ID
    TRACE_ID_REQUEST_HEADER_KEY: str = 'X-Request-ID'

    # CORS Setting
    MIDDLEWARE_CORS: bool = True
    CORS_ALLOWED_ORIGINS: tuple[str] = ('*',)
    CORS_EXPOSE_HEADERS: tuple[str] = (TRACE_ID_REQUEST_HEADER_KEY,)


class LogSettings(BaseSettings):
    """Logs Settings"""

    model_config = SettingsConfigDict(env_prefix='LOG_')

    ROOT_LEVEL: str = 'NOTSET'
    STD_FORMAT: str = (
        '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</> | <lvl>{level: <8}</> | '
        '<cyan> {correlation_id} </> | <lvl>{message}</>'
    )
    LOGURU_FORMAT: str = (
        '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</> | <lvl>{level: <8}</> | '
        '<cyan> {correlation_id} </> | <lvl>{message}</>'
    )
    CID_DEFAULT_VALUE: str = '-'
    CID_UUID_LENGTH: int = 32  # must <= 32
    STDOUT_LEVEL: str = 'INFO'
    STDERR_LEVEL: str = 'ERROR'
    STDOUT_FILENAME: str = 'api_access.log'
    STDERR_FILENAME: str = 'api_error.log'
