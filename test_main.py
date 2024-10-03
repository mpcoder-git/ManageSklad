import pytest
from fastapi.testclient import TestClient

from main import app, get_all_products, get_product, root


client = TestClient(app)


def test_root():
    response = client.get("/")
    #response = root()
    assert response.status_code == 200
    assert response.json() == {"app": "work!!!"}

def test_list_products():
    response = client.get("/products")
    #response = get_all_products()
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    #assert response.json() == {"status": "success"}

def test_get_product():
    response = client.get("/products/1")
    #response = get_product(1)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "prodname": "Product 1", "description": "Description 1", "price": 100.0, "stock": 10.0}

@pytest.mark.skip(reason="отключен чтоб не добавлять лишних строк")
def test_create_product():
    request_data = {"prodname": "Product 7", "description": "Description 7", "price": 200, "stock": 11}
    response = client.post("/products",  json=request_data)
    assert response.status_code == 201
    assert response.json() == {"id": response.json()["id"] ,"prodname": "Product 7", "description": "Description 7", "price": 200, "stock": 11}

def test_update_product():
    request_data = {"prodname": "Product 7", "description": "Description 7", "price": 200, "stock": 11}
    with TestClient(app) as client:
        response = client.put("/products/2",  json=request_data)
    assert response.status_code == 200
    assert response.json() == {"id": response.json()["id"] ,"prodname": "Product 7", "description": "Description 7", "price": 200, "stock": 11}



def test_create_order():
    request_data = {"datecreate": "2023-10-20T16:00:00", "status_id": 1, "order_items": [{"product_id": 1, "quantity": 5.0}]}
    response = client.post("/orders",  json=request_data)
    assert response.status_code == 200
    assert response.json() == { "datecreate": "2023-10-20T16:00:00", "status_id": 1, "order_items": [{"product_id": 1, "quantity": 5.0}]}

def test_get_orders():
    response = client.get("/orders")
    assert response.status_code == 200
    assert response.json()["status"] == "success"

