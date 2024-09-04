from httpx import AsyncClient
from tests.conftest import client


def test_create_product():
    response = client.post("/product/create", json={
        "name": "string1",
        "price": 0.0,
        "is_active": True
    })
    assert response.status_code == 200



async def test_update_product(ac: AsyncClient):
    response = await ac.put("/product/1/", json={
        "name": "string2",
        "price": 1.0,
        "is_active": True
    })

    assert response.status_code == 200


async def test_get_all_products(ac: AsyncClient):
    response = await ac.get("/product/products/")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_product(ac: AsyncClient):
    response = await ac.get("/product/1/")

    assert response.status_code == 200
    assert response.json()["name"] == "string2"


async def test_delete_product(ac: AsyncClient):
    response = await ac.delete("/product/1/")

    assert response.status_code == 200