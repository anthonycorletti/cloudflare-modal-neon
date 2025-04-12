import os

from fastapi import FastAPI
from modal import App, Image, Secret, asgi_app

app = App(name="cloudflare-modal-neon")
app_secrets = [Secret.from_name(f"env-{os.environ['APP_ENV']}")]


image = (
    Image.debian_slim()
    .pip_install(["uv"])
    .workdir("/root")
    .env({"UV_PROJECT_ENVIRONMENT": "/usr/local"})
    .add_local_file("pyproject.toml", "/root/pyproject.toml", copy=True)
    .add_local_file("uv.lock", "/root/uv.lock", copy=True)
    .add_local_python_source("app", copy=True)
    .run_commands(["uv sync --no-dev --frozen --compile-bytecode", "uv build"])
)


@app.function(image=image, timeout=30, secrets=app_secrets)
@asgi_app(label="server")
def server() -> FastAPI:
    from app.main import app

    return app
