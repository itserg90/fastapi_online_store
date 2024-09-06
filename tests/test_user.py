from httpx import AsyncClient
from tests.conftest import client


def test_register():
    response = client.post(
        "/auth/register",
        json={
            "email": "user@test.com",
            "password": "Stringgg!",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "full_name": "string",
            "phone": "+79999999999",
        },
    )

    assert response.status_code == 201


async def test_get_user(ac: AsyncClient):
    response = await ac.get("/users/1/")

    assert response.status_code == 200
    assert response.json()["email"] == "user@test.com"
