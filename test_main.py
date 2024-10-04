from wsgiref.validate import assert_

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

#@pytest.mark.skip(reason="отключен")
def test_get_product():
    response = client.get("/products/2")
    #response = get_product(1)
    assert response.status_code == 200
    assert response.json() == {"id": 2, "prodname": "Product 7", "description": "Description 7", "price": 200.0, "stock": 11.0}

#@pytest.mark.skip(reason="отключен чтоб не добавлять лишних строк")
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
    request_data = {"datecreate": "2022-05-12T13:00:00", "status_id": 1, "order_items": [{"product_id": 1, "quantity": 2}]}
    response = client.post("/orders",  json=request_data)
    expected_response = {
        "datecreate": "2022-05-12T13:00:00",
        "status_id": 1,
        "order_items": [{"product_id": 1, "quantity": 2}]
    }
    assert response.status_code == 200
    assert "datecreate" in response.json()
    assert response.json() == expected_response
    #assert response.json()["datecreate"] == "2022-05-12T13:00:00"



def test_get_orders():
    response = client.get("/orders")
    assert response.status_code == 200
    assert response.json()["status"] == "success"



def test_update_orderstatus():
    request_data = {"status_id": 2}
    response = client.put("/orders/3",  json=request_data)
    assert response.status_code == 200
    assert response.json()["id"] == 3
    assert response.json()["status_id"] == 2