from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models import User
from src.user import crud
from src.user.base_config import current_user, get_current_admin_user
from src.user.schemas import UserRead

router = APIRouter(prefix="/users", tags=["User"])


# @router.get("/users/", response_model=List[UserRead])
# async def get_all_users(user: User = Depends(current_user),
#                         session: AsyncSession = Depends(get_async_session)
#                         ):
#     query = select(User)
#     result = await session.execute(query)
#     return result.scalars().all()


@router.get("/{user_id}/", response_model=UserRead)
async def get_user(
    user_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if user_id == user.id:
        return await crud.get_user(user_id, session)
    raise HTTPException(status_code=404, detail="You have no rights")


@router.put("/add_product/")
async def add_product_to_basket(
    user_id: int,
    product_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if user_id == user.id:
        await crud.add_product_to_basket(user_id, product_id, session)
        return {"message": "Product added to basket"}
    raise HTTPException(status_code=404, detail="You have no rights")


# @router.put("/update_user")
# async def update_user(user_id: int, is_admin: bool, user: User = Depends(current_user),
#                                 session: AsyncSession = Depends(get_async_session)
#                                 ):
#     if user_id == user.id:
#         query_user = select(User).where(User.id == user_id)
#         result_user = await session.execute(query_user)
#         db_user = result_user.scalars().one()
#         db_user.is_admin = is_admin
#
#         await session.commit()
#         return {"message": "Is_admin - True"}
#     raise HTTPException(status_code=404, detail="You have no rights")


@router.put("/delete_product/")
async def delete_product_from_basket(
    user_id: int,
    product_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if user_id == user.id:
        await crud.delete_product_from_basket(user_id, product_id, session)
        return {"message": "Product removed from basket"}
    raise HTTPException(status_code=404, detail="You have no rights")


@router.put("/delete_all_products/")
async def delete_all_products_from_basket(
    user_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if user_id == user.id:
        await crud.delete_all_products_from_basket(user_id, session)
        return {"message": "All products removed from basket"}
    raise HTTPException(status_code=404, detail="You have no rights")
