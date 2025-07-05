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
    CORS_ORIGINS: str = "https://127.0.0.1:5173,https://logfire-api.pydantic.dev"

    # Base URL for the backend. Used by generate_external_api_url to
    # generate URLs to the backend accessible from the outside.
    SERVER_API_BASE_URL: str = "https://127.0.0.1:8000"

    # URL to frontend client app.
    WEB_BASE_URL: str = "https://127.0.0.1:5173"

    # postgres
    POSTGRES_SCHEME: str = "postgresql+asyncpg"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PWD: str = "postgres"
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432
    POSTGRES_DATABASE: str = "postgres"
    POSTGRES_POOL_SIZE: int = 5
    POSTGRES_POOL_RECYCLE_SECONDS: int = 600  # 10 minutes

    # Modal OTEL
    MODAL_OTEL_EXPORTER_OTLP_ENDPOINT: str = "otlp-collector.modal.local:4317"
    MODAL_OTEL_EXPORTER_OTLP_INSECURE: str = "true"
    MODAL_OTEL_EXPORTER_OTLP_PROTOCOL: str = "http/protobuf"

    # Sentry
    SENTRY_DSN: str | None = None

    # Sendgrid
    SENDGRID_API_KEY: str = ""

    # Logfire
    LOGFIRE_TOKEN: str = ""
    OTEL_EXPORTER_OTLP_TRACES_ENDPOINT: str = (
        "https://logfire-api.pydantic.dev/v1/traces"
    )
    OTEL_EXPORTER_OTLP_METRICS_ENDPOINT: str = (
        "https://logfire-api.pydantic.dev/v1/metrics"
    )

    model_config = SettingsConfigDict(
        env_prefix="app_",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_file=environment_file,
        extra="allow",
    )

    @cached_property
    def postgres_dsn(self) -> str:
        path = self.POSTGRES_DATABASE
        if self.is_test() or self.is_local():
            path += f"_{self.ENV.value}"
        return str(
            PostgresDsn.build(
                scheme=self.POSTGRES_SCHEME,
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PWD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=path,
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
