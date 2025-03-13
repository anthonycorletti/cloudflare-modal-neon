import os
from enum import Enum
from functools import cached_property

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    test = "test"
    local = "local"
    preview = "preview"
    production = "production"


environment = Environment(os.getenv("APP_ENV", Environment.local.value))
environment_file = f".env.{environment.value}"


class Settings(BaseSettings):
    ENV: Environment = Environment.local
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    SECRET_KEY: str = "theanswertolifeeverythingandtheuniverseis42"

    # Comma separated list of origins that are allowed to make
    CORS_ORIGINS: str = "http://127.0.0.1:5173"

    # Base URL for the backend. Used by generate_external_api_url to
    # generate URLs to the backend accessible from the outside.
    SERVER_API_BASE_URL: str = "http://127.0.0.1:8000"

    # URL to frontend client app.
    WEB_BASE_URL: str = "http://127.0.0.1:5173"

    # postgres
    POSTGRES_SCHEME: str = "postgresql+asyncpg"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PWD: str = "postgres"
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432
    POSTGRES_DATABASE: str = "postgres"
    POSTGRES_POOL_SIZE: int = 5
    POSTGRES_POOL_RECYCLE_SECONDS: int = 600  # 10 minutes

    # Sentry
    SENTRY_DSN: str | None = None

    # Sendgrid
    SENDGRID_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_prefix="app_",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_file=environment_file,
        extra="allow",
    )

    @cached_property
    def postgres_dsn(self) -> str:
        return str(
            PostgresDsn.build(
                scheme=self.POSTGRES_SCHEME,
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PWD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DATABASE + f"_{self.ENV.value}",
            )
        )

    def is_environment(self, environment: Environment) -> bool:
        return self.ENV == environment

    def is_test(self) -> bool:
        return self.is_environment(Environment.test)

    def is_local(self) -> bool:
        return self.is_environment(Environment.local)

    def is_preview(self) -> bool:
        return self.is_environment(Environment.preview)

    def is_production(self) -> bool:
        return self.is_environment(Environment.production)


settings = Settings()
