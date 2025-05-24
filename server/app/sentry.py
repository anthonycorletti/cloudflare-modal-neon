import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

from app.settings import settings


def configure_sentry() -> None:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        enable_tracing=False,
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1,
        environment=settings.ENV.value,
        integrations=[FastApiIntegration(transaction_style="endpoint")],
        _experiments={"enable_logs": True},
    )
