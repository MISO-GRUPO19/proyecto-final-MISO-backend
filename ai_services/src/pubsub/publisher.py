import os
from google.cloud import pubsub_v1
import json

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'pubsub/proyecto-final-451719-1806c6f593e4.json'

def publish_message(topic_name, data):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path('proyecto-final-451719', topic_name)
    
    data = json.dumps(data).encode('utf-8')
    future = publisher.publish(topic_path, data)
    print(f'Published message ID: {future.result()}')