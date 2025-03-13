from typing import List, Sequence

from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response, status

from app.items.schemas import ItemsCreate, ItemsUpdate
from app.items.service import ItemsService
from app.kit.postgres import AsyncSession, get_async_db_session
from app.models import Items

router = APIRouter(tags=["items"])


class Paths:
    list_items = "/items"
    create_item = "/items"
    new_item = "/items/new"
    show_item = "/items/{item_name}"
    update_item = "/items/{item_name}"
    delete_item = "/items/{item_name}"


@router.get(Paths.list_items, response_model=List[Items])
async def list_items(
    items_svc: ItemsService = Depends(ItemsService),
    db: AsyncSession = Depends(get_async_db_session),
) -> Sequence[Items]:
    data = await items_svc.list_items(db=db)
    return data


@router.get(Paths.show_item, response_model=Items)
async def show_item(
    item_name: str,
    items_svc: ItemsService = Depends(ItemsService),
    db: AsyncSession = Depends(get_async_db_session),
) -> Items:
    data = await items_svc.get_item(db=db, item_name=item_name)
    if not data:
        raise HTTPException(status_code=404, detail="Item not found")
    return data


@router.post(Paths.create_item, response_model=Items)
async def create_item(
    request: Request,
    items_create: ItemsCreate = Body(
        ..., example=ItemsCreate.Config.json_schema_extra["example"]
    ),
    items_svc: ItemsService = Depends(ItemsService),
    db: AsyncSession = Depends(get_async_db_session),
) -> Items:
    if await items_svc.get_item(db=db, item_name=items_create.name):
        raise HTTPException(status_code=409, detail="Item already exists")
    data = await items_svc.create_item(db=db, items_create=items_create)
    return data


@router.put(Paths.update_item, response_model=Items)
async def update_item(
    request: Request,
    item_name: str,
    item_update: ItemsUpdate = Body(
        ..., example=ItemsUpdate.Config.json_schema_extra["example"]
    ),
    items_svc: ItemsService = Depends(ItemsService),
    db: AsyncSession = Depends(get_async_db_session),
) -> Items:
    item = await items_svc.get_item(db=db, item_name=item_name)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    data = await items_svc.update_item(db=db, item=item, items_update=item_update)
    return data


@router.delete(Paths.delete_item, response_model=None)
async def delete_item(
    item_name: str,
    items_svc: ItemsService = Depends(ItemsService),
    db: AsyncSession = Depends(get_async_db_session),
) -> Response:
    if not await items_svc.get_item(db=db, item_name=item_name):
        raise HTTPException(status_code=204, detail="No Content")
    await items_svc.delete_item(db=db, item_name=item_name)
    return Response(status_code=status.HTTP_200_OK)
