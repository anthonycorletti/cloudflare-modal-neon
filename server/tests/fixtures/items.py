import pytest_asyncio

from app.items.schemas import ItemsBase, ItemsCreate, ItemsUpdate


@pytest_asyncio.fixture
async def items_create() -> ItemsCreate:
    return ItemsCreate.model_validate(ItemsBase.Config.json_schema_extra["example"])


@pytest_asyncio.fixture
async def items_update(name: str = "new-name", count: int = 10) -> ItemsUpdate:
    return ItemsUpdate.model_validate(
        {
            **ItemsBase.Config.json_schema_extra["example"],
            **{"name": name, "count": count},
        }
    )
