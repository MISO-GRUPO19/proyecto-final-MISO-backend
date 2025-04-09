#!/bin/bash

# Agregar el directorio raíz al PYTHONPATH
export PYTHONPATH=/authentications_management/src

# Iniciar el servicio de users en segundo plano
flask --app main.py --debug run --host=0.0.0.0 --port=5003 &

# Iniciar el suscriptor
python pubsub/subscriber.py