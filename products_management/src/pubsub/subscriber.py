from google.cloud import pubsub_v1
import json
import os
from models.products import Products, ProductWarehouse, Warehouses 
from models.batches import Batches
from models.database import db_session
import random


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'pubsub/proyecto-final-451719-1806c6f593e4.json'
WAREHOUSE_NAMES = ["Bodega A1", "Bodega A2", "Bodega A3", "Bodega A4", "Bodega A5"]
WAREHOUSE_ADDRESSES = [
    "Calle 123 #45-67, Bogotá, Colombia",
    "Avenida Siempre Viva 742, Medellín, Colombia",
    "Carrera 10 #20-30, Cali, Colombia",
    "Diagonal 25 #15-50, Barranquilla, Colombia",
    "Transversal 8 #12-34, Cartagena, Colombia"
]
SHELF_VALUES = ["A", "B", "C", "D", "E"]
AISLE_VALUES = ["1", "2", "3", "4", "5"]
LEVEL_VALUES = [1, 2, 3]
QUANTITY_WAREHOUSES = random.randint(1, 5)

def create_warehouses():
        existing_warehouses = db_session.query(Warehouses).all()
        if len(existing_warehouses) > 0:
            return existing_warehouses
        else:
            new_whs = []
            for i in range(QUANTITY_WAREHOUSES):
                warehouse = Warehouses(
                    WAREHOUSE_NAMES[random.randint(0, 4)],
                    WAREHOUSE_ADDRESSES[random.randint(0, 4)]
                )
                db_session.add(warehouse)
                db_session.commit()
                new_whs.append(warehouse)
            return new_whs

def create_product_warehouse(product: Products, warehouses, quantity):
    warehouse = random.choice(warehouses)
    product_warehouse = ProductWarehouse(
        product.id,
        warehouse.id,
        product.barcode,
        warehouse.name,
        warehouse.address,
        quantity,
        random.choice(SHELF_VALUES),
        random.choice(AISLE_VALUES),
        random.choice(LEVEL_VALUES)
    )
    db_session.add(product_warehouse)
    db_session.commit()

def callback(message):
    data = json.loads(message.data)
    valid_products = data['valid_products']
    
    try:
        products = []
        batches = []
        warehouses = create_warehouses()
        for row in valid_products:
                        
            product = Products(
                name=row['name'],
                description=row['description'],
                price=row['price'],
                category=row['category'],
                weight=row['weight'],
                barcode=row['barcode'],
                provider_id=row['provider_id'],
            )
            products.append(product)
            

        db_session.add_all(products)
        db_session.flush()

        for product, row in zip(products, valid_products):
            batch = Batches(
                batch=row['batch'],
                best_before=row['best_before'],
                quantity=row['quantity'],
                product_id=product.id
            )
            batches.append(batch)
            create_product_warehouse(product, warehouses, row['quantity'])

        db_session.add_all(batches)
        db_session.commit()

        print(f'{len(valid_products)} productos cargados correctamente')
    except Exception as e:
        db_session.rollback()
        print(f'Error: {e}')
    finally:
        db_session.remove()
    
    message.ack()

def subscribe(subscription_name):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path('proyecto-final-451719', subscription_name)
    
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f'Listening for messages on {subscription_path}...')

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        streaming_pull_future.result()

if __name__ == '__main__':
    subscribe('products-sub')