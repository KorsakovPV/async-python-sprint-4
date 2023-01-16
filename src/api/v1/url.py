from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemes import urls_scheme
from services.url_service import url_crud

router = APIRouter()


@router.get("/", response_model=List[urls_scheme.UrlReadSchema], status_code=status.HTTP_200_OK)
async def read_urls(
        *,
        db: AsyncSession = Depends(get_session),
        skip: int = 0,
        limit: int = 100
) -> Any:
    """
    Retrieve entities.
    """
    urls = await url_crud.get_multi(db=db, skip=skip, limit=limit)
    return urls


@router.get("/{id}", response_model=urls_scheme.UrlReadSchema, status_code=status.HTTP_200_OK)
async def read_url(
        *,
        db: AsyncSession = Depends(get_session),
        id: UUID,
) -> Any:
    """
    Get by ID.
    """
    url = await url_crud.get(db=db, id=id)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return url


@router.post("/", response_model=urls_scheme.UrlReadSchema, status_code=status.HTTP_201_CREATED)
async def create_url(
        *,
        url_in: urls_scheme.UrlCreateSchema,
        db: AsyncSession = Depends(get_session),
) -> Any:
    """
    Create new entity.
    """
    # create item by params
    url = await url_crud.create(db=db, obj_in=url_in)
    return url


@router.post(
    "/multi",
    response_model=List[urls_scheme.UrlReadSchema],
    status_code=status.HTTP_201_CREATED
)
async def create_urls(
        *,
        urls_in: List[urls_scheme.UrlCreateSchema],
        db: AsyncSession = Depends(get_session),
) -> Any:
    """
    Create new entity.
    """
    # create item by params
    urls = await url_crud.create_multi(db=db, obj_in=urls_in)
    return urls


@router.put("/{id}", response_model=urls_scheme.UrlReadSchema, status_code=status.HTTP_200_OK)
async def update_urls(
        *,
        db: AsyncSession = Depends(get_session),
        id: UUID,
        url_in: urls_scheme.UrlEditSchema,
) -> Any:
    """
    Update an entity.
    """
    # get item from db
    url = await url_crud.get(db=db, id=id)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    # update item in db
    url = await url_crud.update(db=db, db_obj=url, obj_in=url_in)
    return url


@router.delete("/{id}", response_model=urls_scheme.UrlReadSchema, status_code=status.HTTP_410_GONE)
async def delete_url(
        *,
        db: AsyncSession = Depends(get_session),
        id: UUID
) -> Any:
    """
    Delete an entity.
    """
    # get item from db
    url = await url_crud.get(db=db, id=id)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    # remove item from db
    url = await url_crud.delete(db=db, db_obj=url)
    return url
