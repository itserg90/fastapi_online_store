from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select, delete

from src.models import Product
from src.product.schemas import ProductCreate, ProductUpdate


async def get_product(product_id: int, session):
    """Получает товар"""
    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    db_product = result.scalars().first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


async def get_all_products(session):
    """Получает все товары"""
    query = select(Product).where(Product.is_active == True)
    result = await session.execute(query)
    return result.scalars().all()


async def create_product(new_product: ProductCreate, session):
    """Создает новый товар"""
    stmt = Product(**new_product.model_dump())
    session.add(stmt)
    await session.flush()
    await session.commit()


async def update_product(product_id: int, product: ProductUpdate, session):
    """Обновляет товар"""
    query = select(Product).filter(Product.id == product_id)
    result = await session.execute(query)
    db_product = result.scalars().one()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    current_time = datetime.utcnow()
    db_product.name = product.name
    db_product.price = product.price
    db_product.is_active = product.is_active
    db_product.updated_at = current_time

    await session.commit()


async def delete_product(product_id: int, session):
    """Удаляет товар"""
    query = delete(Product).filter(Product.id == product_id)
    await session.execute(query)

    await session.commit()
