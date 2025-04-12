import io
import json
from flask_jwt_extended import create_access_token
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from products_management.src.api.products import products

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(products)
    
    # Necesario para @jwt_required
    app.config["JWT_SECRET_KEY"] = "qwerty"
    from flask_jwt_extended import JWTManager
    JWTManager(app)

    with app.test_client() as client:
        yield client


@patch("products_management.src.api.products.CreateProducts")
def test_create_product_success(mock_create_products, client):
    mock_create_products.return_value.execute.return_value = {"message": "Producto creado"}
    
    token = create_access_token(identity="user-id")
    headers = {'Authorization': f'Bearer {token}'}
    
    response = client.post(
        "/products",
        json={"name": "Producto A"},
        headers=headers
    )

    assert response.status_code == 201
    assert response.json == {"message": "Producto creado"}


@patch("products_management.src.api.products.CreateProducts")
def test_create_product_invalid_data(mock_create_products, client):
    from products_management.src.errors.errors import InvalidData
    mock_create_products.return_value.execute.side_effect = InvalidData(errors={"name": "Requerido"})

    token = create_access_token(identity="user-id")
    headers = {'Authorization': f'Bearer {token}'}
    
    response = client.post(
        "/products",
        json={},
        headers=headers
    )

    assert response.status_code == 400
    assert "error" in response.json
    assert response.json["error"] == "Datos inválidos"
    assert response.json["detalles"] == {"name": "Requerido"}


@patch("products_management.src.api.products.CreateProducts")
def test_create_product_unexpected_error(mock_create_products, client):
    mock_create_products.return_value.execute.side_effect = Exception("Algo falló")
    
    token = create_access_token(identity="user-id")
    headers = {'Authorization': f'Bearer {token}'}
    
    response = client.post(
        "/products",
        json={},
        headers=headers
    )

    assert response.status_code == 500
    assert response.json["error"] == "Ocurrió un error inesperado"


@patch("products_management.src.api.products.CreateMassiveProducts")
def test_upload_products_success(mock_massive, client):
    mock_massive.return_value.execute.return_value = ({"message": "OK"}, 201)
    
    data = {
        'file': (io.BytesIO(b"contenido de prueba"), 'products.csv')
    }
    token = create_access_token(identity="user-id")
    headers = {'Authorization': f'Bearer {token}'}
    
    response = client.post(
        "/products/upload_products",
        content_type='multipart/form-data',
        data=data,
        headers=headers
    )

    assert response.status_code == 201
    assert response.json["message"] == "OK"


@patch("products_management.src.api.products.GetProducts")
def test_get_products_success(mock_get_products, client):
    mock_get_products.return_value.execute.return_value = [
        {"name": "Producto A", "barcode": "123", "stock": 10, "price": 5.5}
    ]
    token = create_access_token(identity="user-id")
    headers = {'Authorization': f'Bearer {token}'}
    
    response = client.get(
        "/products",
        headers=headers
    )

    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert response.json[0]["name"] == "Producto A"


def test_ping(client):
    response = client.get("/products/ping")
    assert response.status_code == 200
    assert response.json == {"message": "pong"}
