from httpx import AsyncClient


async def test_liveliness_check(client: AsyncClient) -> None:
    response = await client.get("/livez")
    assert response.status_code == 200


async def test_readiness_check(client: AsyncClient) -> None:
    response = await client.get("/readyz")
    assert response.status_code == 200
    assert response.json()["message"] == "All systems go."
