import json
from typing import Dict

from fastapi import FastAPI
from modal import App, Image, Secret, asgi_app

from app.settings import settings

app = App(name="cloudflare-modal-neon")

_app_env_dict: Dict[str, str | None] = {
    f"APP_{str(k)}": str(v) for k, v in json.loads(settings.model_dump_json()).items()
}
app_secrets = Secret.from_dict(_app_env_dict)

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


@app.function(image=image, timeout=30, secrets=[app_secrets])
@asgi_app(label="server")
def server() -> FastAPI:
    from app.main import app

    return app
