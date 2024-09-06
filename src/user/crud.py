from fastapi import Depends, HTTPException

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User, Product
from src.database import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Получает базу данных пользователей"""
    yield SQLAlchemyUserDatabase(session, User)


async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    """Получает информацию о пользователе с его корзиной и общей стоимостью товаров"""
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    total = await get_total_price(db_user.products)
    db_user.total_price_of_products = total
    return db_user


async def get_total_price(products):
    """Получает общую стоимость товаров в корзине"""
    return sum([product.price for product in products])


async def add_product_to_basket(
    user_id: int, product_id: int, session: AsyncSession = Depends(get_async_session)
):
    """Добавляет товар в корзину"""
    query_user = select(User).where(User.id == user_id)
    result_user = await session.execute(query_user)
    db_user = result_user.scalars().one()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    query_product = select(Product).where(Product.id == product_id)
    result_product = await session.execute(query_product)
    db_product = result_product.scalars().one()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_user.products.append(db_product)
    await session.commit()


async def delete_product_from_basket(
    user_id: int, product_id: int, session: AsyncSession = Depends(get_async_session)
):
    """Удаляет товар из корзины"""
    query_user = select(User).where(User.id == user_id)
    result_user = await session.execute(query_user)
    db_user = result_user.scalars().one()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for product in db_user.products:
        if product.id == product_id:
            db_user.products.remove(product)
    await session.commit()


async def delete_all_products_from_basket(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    """Удаляет все товары из корзины"""
    query_user = select(User).where(User.id == user_id)
    result_user = await session.execute(query_user)
    db_user = result_user.scalars().one()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.products = []

    await session.commit()
