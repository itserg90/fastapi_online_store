from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (
    String,
    TIMESTAMP,
    MetaData, ForeignKey, Integer, Column, Boolean, Float, ARRAY
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column

metadata = MetaData()
Base = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)

    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    hashed_password = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

    products = relationship("Product", secondary="product_user", backref='products', lazy="selectin")
    total_price_of_products = Column(Float, nullable=True)

    is_admin: bool = Column(Boolean, default=False)


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class ProductUser(Base):
    __tablename__ = "product_user"
    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey("product.id"), nullable=False)
    user_id = Column(ForeignKey("user.id"), nullable=False)
