from google.cloud import pubsub_v1
import json
import os
from models.users import Users
from models.database import db_session

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'pubsub/proyecto-final-451719-1806c6f593e4.json'

def callback(message):
    try:
        # Decodificar el mensaje recibido
        data = json.loads(message.data)
        email = data.get('email')
        role = data.get('role')
        password = data.get('password')

        # Validar que los campos necesarios estén presentes
        if not email or not role or not password:
            raise ValueError("Faltan campos obligatorios en el mensaje")

        # Crear el usuario en la base de datos
        user = Users(
            email=email,
            role=role,
            password=password
        )
        db_session.add(user)
        db_session.commit()

        print(f'Usuario creado exitosamente: {email}')
        message.ack()  # Confirmar que el mensaje fue procesado correctamente
    except Exception as e:
        db_session.rollback()
        print(f'Error al procesar el mensaje: {e}')
        message.nack()  # Indicar que el mensaje no fue procesado correctamente
    finally:
        db_session.close()

def subscribe(subscription_name):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path('proyecto-final-451719', subscription_name)
    
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f'Escuchando mensajes en {subscription_path}...')

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        streaming_pull_future.result()

if __name__ == '__main__':
    subscribe('users-sub')