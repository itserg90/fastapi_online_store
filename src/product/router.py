from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models import User

from src.product import crud
from src.product.schemas import ProductCreate, ProductUpdate, ProductRead
from src.user.base_config import get_current_admin_user, current_user

router = APIRouter(prefix="/product", tags=["Product"])


@router.get("/products/")
async def get_all_products(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.get_all_products(session)


@router.get("/{product_id}/", response_model=ProductRead)
async def get_product(
    product_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.get_product(product_id, session)


@router.post("/create/")
async def create_product(
    new_product: ProductCreate,
    user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_async_session),
):
    await crud.create_product(new_product, session)
    return {"status": "success"}


@router.put("/{product_id}/")
async def update_product(
    product_id: int,
    product: ProductUpdate,
    # user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_async_session),
):
    await crud.update_product(product_id, product, session)
    return {"status": "success"}


@router.delete("/{product_id}/")
async def delete_product(
    product_id: int,
    # user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_async_session),
):
    await crud.delete_product(product_id, session)
    return {"status": "success"}
