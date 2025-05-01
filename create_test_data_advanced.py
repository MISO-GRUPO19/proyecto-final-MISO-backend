import argparse
import requests
import random
import time
import json
from faker import Faker
from datetime import datetime, timedelta
from pathlib import Path
import re

faker = Faker()

# Configuración de constantes
DEV_URL = "http://127.0.0.1:8080"
PRD_URL = "https://nginx-service-230506421700.us-central1.run.app"

ADMIN_EMAIL = "admin@ccp.com"
ADMIN_PASSWORD = "Admin123-"

PROVIDER_ID = "697d7c97-ac98-4179-a89d-57fe3d1c7c3a"
ROUTE_ID = "123e4567-e89b-12d3-a456-426614174003"

# Inicialización de resumen y log
summary = {
    "users": [],
    "customers": [],
    "sellers": [],
    "manufacturers": [],
    "products": [],
    "orders": []
}
log_path = Path("log.txt")


def log(message):
    print(message)
    with open(log_path, "a") as f:
        f.write(message + "\n")


def get_base_urls(env):
    base = DEV_URL if env == "dev" else PRD_URL
    return {
        "login": f"{base}/users/login",
        "create_user": f"{base}/users",
        "create_customer": f"{base}/users/customers",
        "create_seller": f"{base}/users/sellers",
        "create_manufacturer": f"{base}/manufacturers",
        "get_manufacturers": f"{base}/manufacturers",
        "create_product": f"{base}/products",
        "create_order": f"{base}/orders"
    }


def login(urls):
    response = requests.post(urls["login"], json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    if response.status_code == 200:
        token = response.json()['access_token']
        log("✅ Login exitoso.")
        return token
    else:
        raise Exception(f"❌ Error en login: {response.status_code} - {response.text}")


def create_user(urls, token, email, password):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "email": email,
        "password": password,
        "confirm_password": password,
        "role": 3
    }
    response = requests.post(urls["create_user"], json=payload, headers=headers)
    if response.status_code in (201, 409):
        log(f"✅/⚠️ Usuario {email} procesado.")
    else:
        raise Exception(f"❌ Error al crear usuario: {response.status_code} - {response.text}")


def create_customer(urls, token, user_data):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "firstName": user_data["firstName"],
        "lastName": user_data["lastName"],
        "country": user_data["country"],
        "address": user_data["address"],
        "phoneNumber": user_data["phoneNumber"],
        "email": user_data["email"]
    }
    response = requests.post(urls["create_customer"], json=payload, headers=headers)
    if response.status_code == 201:
        customer_id = response.json()["customer_id"]
        log(f"✅ Cliente {user_data['email']} creado. ID: {customer_id}")
        return customer_id
    else:
        raise Exception(f"❌ Error al crear cliente: {user_data} {response.status_code} - {response.text}")


def create_seller(urls, token, seller_data):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(urls["create_seller"], json=seller_data, headers=headers)
    if response.status_code == 201:
        seller_id = response.json()["id"]
        log(f"✅ Vendedor {seller_data['name']} creado. ID: {seller_id}")
        return seller_id
    else:
        raise Exception(f"❌ Error al crear vendedor: {seller_data} {response.status_code} - {response.text}")


def create_manufacturer(urls, token, name, country, contact, telephone, email):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": name,
        "country": country,
        "contact": contact,
        "telephone": telephone,
        "email": email
    }
    response = requests.post(urls["create_manufacturer"], json=payload, headers=headers)
    if response.status_code == 201:
        manufacturer_id = response.json().get("id", faker.uuid4())
        log(f"✅ Fabricante {name} creado. ID: {manufacturer_id}")
        return manufacturer_id
    else:
        raise Exception(f"❌ Error al crear fabricante: {name} - {response.status_code} - {response.text}")


def get_manufacturers(urls, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(urls["get_manufacturers"], headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"❌ Error al obtener fabricantes: {response.status_code} - {response.text}")


def create_product(urls, token, manufacturer_id):
    headers = {"Authorization": f"Bearer {token}"}
    category = random.choice([
        "Frutas y Verduras", "Carnes y Pescados", "Lácteos y Huevos",
        "Panadería y Repostería", "Despensa", "Bebidas", "Snacks y Dulces",
        "Condimentos y Especias", "Productos de Limpieza", "Productos para Bebés"
    ])
    payload = {
        "name": faker.word().capitalize() + " " + faker.word().capitalize(),
        "description": faker.sentence(),
        "price": round(random.uniform(1.0, 10.0), 2),
        "category": category,
        "weight": round(random.uniform(0.2, 2.0), 2),
        "barcode": faker.ean13(),
        "provider_id": manufacturer_id,
        "batch": faker.lexify(text='???-###').upper(),
        "best_before": (datetime.now() + timedelta(days=random.randint(180, 720))).isoformat(),
        "quantity": random.randint(50, 500),
    }
    response = requests.post(urls["create_product"], json=payload, headers=headers)
    if response.status_code == 201:
        log(f"✅ Producto '{payload['name']}' creado.")
        return payload
    else:
        raise Exception(f"❌ Error al crear producto: {response.status_code} - {response.text}")
    

def update_order_status(base_url, token, order_id, new_state):
    """Actualiza el estado de una orden usando el endpoint PUT /orders/{id}/status"""
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{base_url}/orders/{order_id}/status"
    payload = {"state": new_state}
    
    try:
        response = requests.put(url, json=payload, headers=headers)
        if response.status_code == 200:
            log(f"✅ Estado de orden {order_id} actualizado a {new_state}")
            return True
        else:
            log(f"⚠️ Error al actualizar orden {order_id} a {new_state}: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        log(f"⚠️ Excepción al actualizar orden {order_id}: {str(e)}")
        return False

def create_order(urls, token, client_id, products, seller_ids):
    """Crea una nueva orden y simula su flujo de estado"""
    headers = {"Authorization": f"Bearer {token}"}
    total = sum(p["price"] * p["quantity"] for p in products)
    
    payload = {
        "client_id": client_id,
        "seller_id": random.choice(seller_ids),
        "date": datetime.now().isoformat(),
        "provider_id": PROVIDER_ID,
        "total": round(total, 2),
        "type": "CLIENTE",
        "route_id": ROUTE_ID,
        "products": [{"barcode": p["barcode"], "quantity": p["quantity"]} for p in products]
    }
    
    try:
        # Crear la orden
        response = requests.post(urls["create_order"], json=payload, headers=headers)
        response.raise_for_status()
        order_data = response.json()
        log(f"Respuesta de crear orden: {order_data}")
        order_id = order_data["id"]
        log(f"✅ Orden {order_id} creada para cliente {client_id} | Total: ${total:.2f}")
        
        # Obtener la URL base (removiendo el path /orders)
        base_url = urls["create_order"].split('/orders')[0]
        
        # Simular flujo de estados con probabilidades
        time.sleep(1)  # Espera antes de cambiar el estado
        
        # Distribución de probabilidad:
        # - 20% Completado (PENDIENTE → ENPORCESO → ENTREGADO)
        # - 70% En proceso (PENDIENTE → ENPORCESO)
        # - 10% Cancelado (PENDIENTE → CANCELADO)
        status_flow = random.choices(
            ["completed", "processing", "canceled"],
            weights=[0.20, 0.70, 0.10],
            k=1
        )[0]
        
        if status_flow == "completed":
            # Flujo completo
            if update_order_status(base_url, token, order_id, "ENPORCESO"):
                time.sleep(1)
                update_order_status(base_url, token, order_id, "ENTREGADO")
                
        elif status_flow == "processing":
            # Solo pasa a ENPORCESO
            update_order_status(base_url, token, order_id, "ENPORCESO")
            
        elif status_flow == "canceled":
            # Se cancela
            update_order_status(base_url, token, order_id, "CANCELADO")
            
        return order_id
        
    except requests.exceptions.RequestException as e:
        error_msg = f"❌ Error al crear orden: {str(e)}"
        if hasattr(e, 'response') and e.response:
            error_msg += f" | Response: {e.response.text}"
        log(error_msg)
        raise Exception(error_msg)
    
def main():
    parser = argparse.ArgumentParser(description="Generador de datos de prueba.")
    parser.add_argument("--users", type=int, default=5)
    parser.add_argument("--sellers", type=int, default=3)
    parser.add_argument("--manufacturers", type=int, default=3)
    parser.add_argument("--products-per-manufacturer", type=int, default=5)
    parser.add_argument("--orders", type=int, default=10)
    parser.add_argument("--env", choices=["dev", "prd"], default="prd")
    args = parser.parse_args()

    if log_path.exists():
        log_path.unlink()

    countries = ["Argentina", "Chile", "Brasil", "Ecuador", "Colombia"]
    selected_country = random.choice(countries)
    log(f"🌎 País seleccionado: {selected_country}")

    try:
        urls = get_base_urls(args.env)
        token = login(urls)

        # Crear vendedores
        for _ in range(args.sellers):
            seller_data = {
                "identification": str(faker.unique.random_number(digits=9)),
                "name": faker.name(),
                "country": selected_country,
                "address": faker.address().replace("\n", ", "),
                "telephone": faker.msisdn()[:10],
                "email": faker.unique.email()
            }
            seller_id = create_seller(urls, token, seller_data)
            summary["sellers"].append(seller_id)

        # Crear usuarios/clientes
        for _ in range(args.users):
            user_data = {
                "email": faker.email(),
                "password": "Admin*1234",
                "firstName": faker.first_name(),
                "lastName": faker.last_name(),
                "country": selected_country,
                "address": faker.address().replace("\n", ", "),
                "phoneNumber": faker.msisdn()[:10]
            }
            if user_data["phoneNumber"][0] == "0":
                user_data["phoneNumber"] = "3" + user_data["phoneNumber"][1:]
            user_data["firstName"] = re.sub(r'[^a-zA-Z\s]', '', user_data["firstName"])
            user_data["lastName"] = re.sub(r'[^a-zA-Z\s]', '', user_data["lastName"])
            
            if len(user_data["firstName"]) < 3:
                user_data["firstName"] = f"User-{user_data['firstName']}"
            if len(user_data["lastName"]) < 3:
                user_data["lastName"] = f"User-{user_data['lastName']}"

            create_user(urls, token, user_data["email"], user_data["password"])
            client_id = create_customer(urls, token, user_data)
            summary["users"].append(user_data["email"])
            summary["customers"].append(client_id)

        # Crear fabricantes
        for _ in range(args.manufacturers):
            name = faker.company()
            name = re.sub(r'[^a-zA-Z\s]', '', name)
            name = re.sub(r'[,\s]+', ' ', name).strip()
            if len(name) < 3:
                name = f"Manufacturer-{name}"
            if len(name) > 100:
                name = name[:100]
            manufacturer_id = create_manufacturer(
                urls, token,
                name=name,
                country=selected_country,
                contact=faker.name(),
                telephone=faker.msisdn()[:10],
                email=faker.company_email()
            )
            summary["manufacturers"].append(manufacturer_id)

        time.sleep(2)

        manufacturers = get_manufacturers(urls, token)
        manufacturer_ids = [m["id"] for m in manufacturers]

        # Crear productos
        for manufacturer_id in manufacturer_ids:
            log(f"🌟 Creando productos para fabricante {manufacturer_id}")
            log(f"Fabricante: {args.products_per_manufacturer}")
            for _ in range(args.products_per_manufacturer):
                product = create_product(urls, token, manufacturer_id)
                summary["products"].append(product)

        # Crear órdenes
        for _ in range(args.orders):
            client_id = random.choice(summary["customers"])
            selected_products = random.sample(summary["products"], random.randint(1, 3))
            for p in selected_products:
                p["quantity"] = random.randint(1, 5)
            create_order(urls, token, client_id, selected_products, summary["sellers"])
            summary["orders"].append({
                "client_id": client_id,
                "products": [p["barcode"] for p in selected_products]
            })

        # Resumen Final
        log("\n📋 Resumen Final:")
        log(json.dumps(summary, indent=2))

    except Exception as e:
        log(f"\n❌ Error general: {e}")


if __name__ == "__main__":
    main()
