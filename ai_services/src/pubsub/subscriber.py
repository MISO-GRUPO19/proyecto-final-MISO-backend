from google.cloud import pubsub_v1
import json
import os
from models.video import Video, VideoStatus
from models.database import db_session

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'pubsub/proyecto-final-451719-1806c6f593e4.json'

def callback(message):
    data = json.loads(message.data.decode('utf-8'))
    video_id = data['video_id']
    
    try:
        video = db_session.query(Video).filter_by(id=video_id).first()
        if not video:
            print(f'Video {video_id} no encontrado')
            message.ack()
            return 
                
        if video.status != VideoStatus.processed:
            video.status = VideoStatus.processed
            video.results = {
                "analisis": [
                    "6 estanterías con productos",
                    "Vacíos en 2 secciones clave",
                    "Visibles: Salsas, Snacks, Energéticas",
                    "Menos visibles: Lácteos y Panadería"
                ],
                "recomendaciones": [
                    "Mover Snacks a la altura de los ojos (+35%)",
                    "Reubicar Energéticas (+20% ventas)",
                    "Reponer Salsa Picante (10), Tomate (15)",
                    "Agregar Chocoboom, MaxPower",
                    "Promoción: Combo Snacks + Bebida Energética"
                ]
            }
            
            db_session.add(video)
            db_session.commit()

            print(f'Video {video_id} actualizado a PROCESADO')
        
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
    subscribe('videos-sub')