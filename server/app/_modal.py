import json
from typing import Dict

from fastapi import FastAPI
from modal import App, Image, Secret, asgi_app

from app.settings import settings

app = App(name="cloudflare-modal-neon")

_app_env_dict: Dict[str, str | None] = {
    f"APP_{str(k)}": str(v) for k, v in json.loads(settings.model_dump_json()).items()
}
_remove_prefix_keys = ["APP_OPENAI_API_KEY"]
for key in _remove_prefix_keys:
    if key in _app_env_dict:
        new_key = key.replace("APP_", "")
        _app_env_dict[new_key] = _app_env_dict[key]

app_env = Secret.from_dict(_app_env_dict)

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


@app.function(
    cpu=0.5,
    memory=256,
    image=image,
    timeout=1800,
    secrets=[app_env],
    min_containers=1,
    scaledown_window=30,
)
@asgi_app(label="server")
def server() -> FastAPI:
    from app.main import app

    return app
