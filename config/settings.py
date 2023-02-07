import os
from functools import lru_cache

from pydantic import BaseSettings, Field, validator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    BASE_DIR: str = BASE_DIR

    PROJECT_NAME: str = Field(default="Listen Backend", env="PROJECT_NAME")
    DEBUG: bool = Field(default=False, env="DEBUG")
    RELOAD: bool = Field(default=False, env="RELOAD")
    HOST: str = Field(default="127.0.0.1", env="HOST")
    PORT: int = Field(default="5000", env="PORT")
    COLOR_LOGS: bool = Field(default=False, env="COLOR_LOGS")
    IS_DOC_ENABLED: bool = Field(default=True, env="IS_DOC_ENABLED")
    CORS_ORIGINS_LIST: str = Field(default="*", env="CORS_ORIGINS_LIST")

    LOGGING_LEVEL_ROOT: str = Field(default="WARNING", env="LOGGING_LEVEL_ROOT")

    LOG_TO_FILE_ENABLED: bool = Field(default=True, env="LOG_TO_FILE_ENABLED")
    LOG_TO_FILE_PATH: str = Field(default=os.path.join(BASE_DIR, "logs"), env="LOG_TO_FILE_PATH")
    LOG_TO_FILE_NAME: str = Field(default="application.log", env="LOG_TO_FILE_NAME")
    LOG_TO_FILE_REQUESTS_ENABLED: bool = Field(default=True, env="LOG_TO_FILE_REQUESTS_ENABLED")
    LOG_TO_FILE_REQUESTS_PATH: str = Field(
        default=os.path.join(BASE_DIR, "logs"), env="LOG_TO_FILE_REQUESTS_PATH"
    )
    LOG_TO_FILE_REQUESTS_NAME: str = Field(
        default="application_requests.log", env="LOG_TO_FILE_REQUESTS_NAME"
    )

    # DB CONFIG
    POSTGRES_HOST: str = Field(default="localhost", env="POSTGRES_HOST")
    POSTGRES_PORT: str = Field(default="5432", env="POSTGRES_PORT")
    POSTGRES_DB: str = Field(default="bondable-backend-postgres", env="POSTGRES_DB")
    POSTGRES_USER: str = Field(default="bondable-backend-postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(default="bondable-backend-postgres", env="POSTGRES_PASSWORD")

    # Pagination Settings
    DEFAULT_LIMIT: int = Field(default=100, env="DEFAULT_LIMIT")
    MIN_LIMIT: int = Field(default=1, env="MIN_LIMIT")
    MAX_LIMIT: int = Field(default=1000, env="MAX_LIMIT")
    MIN_OFFSET: int = Field(default=0, env="MIN_OFFSET")

    # Background tasks config
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")

    # Allowed usernames and emails
    # usernames and emails of users separated by coma
    ALLOWED_USERNAMES_AND_EMAILS: str = Field(default="", env="ALLOWED_USERNAMES_AND_EMAILS")

    class Config:
        env_file = os.path.join(BASE_DIR, ".config", ".env")

    @classmethod
    def _get_list_from_string_values(cls, value, separator: str = ","):
        return [v.strip() for v in value.split(separator)]

    @validator("CORS_ORIGINS_LIST", always=True)
    def set_origins_list(cls, v):
        return cls._get_list_from_string_values(value=v)

    @validator("ALLOWED_USERNAMES_AND_EMAILS", always=True)
    def set_allowed_usernames_and_emails(cls, v):
        return cls._get_list_from_string_values(value=v)


@lru_cache
def get_settings():
    return Settings()
