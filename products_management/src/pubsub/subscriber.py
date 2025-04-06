from google.cloud import pubsub_v1
import json
import uuid
import os
from models.products import Products, Batch
from models.database import db_session

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'pubsub/proyecto-final-451719-1806c6f593e4.json'

def callback(message):
    data = json.loads(message.data)
    valid_products = data['valid_products']
    
    try:
        products = []
        batches = []

        for row in valid_products:
                        
            product = Products(
                name=row['name'],
                description=row['description'],
                price=row['price'],
                category=row['category'],
                weight=row['weight'],
                barcode=row['barcode'],
                provider_id=row['provider_id']
            )
            products.append(product)

        db_session.add_all(products)
        db_session.flush()

        for product, row in zip(products, valid_products):
            batch = Batch(
                batch=row['batch'],
                best_before=row['best_before'],
                quantity=row['quantity'],
                product_id=product.id
            )
            batches.append(batch)

        db_session.add_all(batches)
        db_session.commit()

        print(f'{len(valid_products)} productos cargados correctamente')
    except Exception as e:
        db_session.rollback()
        print(f'Error: {e}')
    finally:
        db_session.close()
    
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