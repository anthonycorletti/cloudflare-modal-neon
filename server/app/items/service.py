from typing import Sequence

from sqlmodel import desc, select

from app.items.schemas import ItemsCreate, ItemsUpdate
from app.kit.postgres import AsyncSession
from app.models import Items


class ItemsService:
    async def list_items(self, db: AsyncSession) -> Sequence[Items]:
        results = await db.exec(select(Items).order_by(desc(Items.updated_at)))
        return results.all()

    async def create_item(self, db: AsyncSession, items_create: ItemsCreate) -> Items:
        item = Items(**items_create.model_dump())
        db.add(item)
        await db.flush()
        return item

    async def get_item(self, db: AsyncSession, item_name: str) -> Items | None:
        item = await db.exec(select(Items).where(Items.name == item_name))
        return item.one_or_none()

    async def delete_item(self, db: AsyncSession, item_name: str) -> None:
        item = await self.get_item(db, item_name)
        if item:
            await db.delete(item)

    async def update_item(
        self, db: AsyncSession, item: Items, items_update: ItemsUpdate
    ) -> Items:
        for key, value in items_update.model_dump().items():
            setattr(item, key, value)
        db.add(item)
        await db.flush()
        return item
