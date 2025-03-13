import uuid

from httpx import AsyncClient

from app.items.schemas import ItemsCreate, ItemsUpdate


async def test_create_items(client: AsyncClient, items_create: ItemsCreate) -> None:
    response = await client.post("/items", json=items_create.model_dump())
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "book"


async def test_list_items(client: AsyncClient, items_create: ItemsCreate) -> None:
    response = await client.get("/items")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == []
    response = await client.post("/items", json=items_create.model_dump())
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "book"
    response = await client.get("/items")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 1
    item = response_json[0]
    assert uuid.UUID(item["id"])
    assert item["name"] == "book"
    assert item["count"] == 1
    assert item["description"] is None
    assert item["created_at"] is not None
    assert item["updated_at"] is not None
    assert item["deleted_at"] is None


async def test_get_item(client: AsyncClient, items_create: ItemsCreate) -> None:
    response = await client.post("/items", json=items_create.model_dump())
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "book"
    response = await client.get("/items/book")
    assert response.status_code == 200
    response_json = response.json()
    item = response_json
    assert uuid.UUID(item["id"])
    assert item["name"] == "book"
    assert item["count"] == 1
    assert item["description"] is None
    assert item["created_at"] is not None
    assert item["updated_at"] is not None
    assert item["deleted_at"] is None


async def test_update_item(
    client: AsyncClient, items_create: ItemsCreate, items_update: ItemsUpdate
) -> None:
    response = await client.post("/items", json=items_create.model_dump())
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "book"
    response = await client.put("/items/book", json=items_update.model_dump())
    assert response.status_code == 200
    response_json = response.json()
    item = response_json
    assert uuid.UUID(item["id"])
    assert item["name"] == "new-name"
    assert item["count"] == 10
    assert item["description"] is None
    assert item["created_at"] is not None
    assert item["updated_at"] is not None
    assert item["deleted_at"] is None


async def test_delete_item(client: AsyncClient, items_create: ItemsCreate) -> None:
    response = await client.post("/items", json=items_create.model_dump())
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "book"
    response = await client.delete("/items/book")
    assert response.status_code == 200
    response = await client.get("/items/book")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "Item not found"


async def test_create_item_fails_name_already_exists(
    client: AsyncClient, items_create: ItemsCreate
) -> None:
    response = await client.post("/items", json=items_create.model_dump())
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "book"
    response = await client.post("/items", json=items_create.model_dump())
    assert response.status_code == 409
    response_json = response.json()
    assert response_json["detail"] == "Item already exists"


async def test_update_item_fails_item_not_found(client: AsyncClient) -> None:
    response = await client.put("/items/book", json={"name": "book", "count": 2})
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "Item not found"


async def test_delete_item_fails_item_not_found(client: AsyncClient) -> None:
    response = await client.delete("/items/book")
    assert response.status_code == 204
