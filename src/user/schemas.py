from typing import Optional, List

from fastapi_users import schemas
from pydantic import field_validator, EmailStr

from src.product.schemas import ProductRead


class UserRead(schemas.BaseUser[int]):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    products: Optional[List[ProductRead]] = None
    total_price_of_products: Optional[float] = None

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    full_name: str
    email: EmailStr
    phone: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        upper_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower_letters = "abcdefghijklmnopqrstuvwxyz"
        symbols = "$%&!:"
        if len(password) > 7:
            if any(char in upper_letters for char in password):
                if any(char in lower_letters for char in password):
                    if any(char in symbols for char in password):
                        return password
        raise ValueError(
            "Пароль должен соответствовать следующим требованиям: "
            "не менее 8 символов, только латиница, "
            "минимум 1 символ верхнего регистра, минимум 1 спец символ ($%&!:).")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, phone: str) -> str:
        if len(phone) == 12:
            if phone.startswith("+7") and phone[2:].isdigit():
                return phone
        raise ValueError("Номер телефона должен начинаться с +7 и содержать 10 цифр.")
