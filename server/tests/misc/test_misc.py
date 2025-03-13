from httpx import AsyncClient

from app.settings import settings


async def test_settings_env_check() -> None:
    assert settings.is_test()
    assert not settings.is_local()
    assert not settings.is_preview()


async def test_get_openapi_json(client: AsyncClient) -> None:
    response = await client.get("/openapi.json")
    assert response.status_code == 200


async def test_get_docs(client: AsyncClient) -> None:
    response = await client.get("/docs")
    assert response.status_code == 200
    assert "swagger-ui" in response.text
    assert "openapi.json" in response.text
