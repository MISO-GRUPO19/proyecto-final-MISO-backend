#!/bin/bash

# Agregar el directorio raíz al PYTHONPATH
export PYTHONPATH=/ai-services/src

# Iniciar el servicio de productos en segundo plano
flask --app main.py --debug run --host=0.0.0.0 --port=5006 &

# Iniciar el suscriptor
python pubsub/subscriber.py