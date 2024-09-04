from fastapi import FastAPI

from src.user.base_config import auth_backend, fastapi_users
from src.user.schemas import UserRead, UserCreate

from src.user.router import router as router_user
from src.product.router import router as router_product


app = FastAPI(title="Trading App")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_user)
app.include_router(router_product)
