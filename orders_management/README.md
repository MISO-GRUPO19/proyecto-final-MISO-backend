# Order Microservice

Este microservicio está diseñado para registrar y gestionar pedidos de productos utilizando Flask.

## Estructura del Proyecto

```
order-microservice
├── src
│   ├── app.py                  # Punto de entrada de la aplicación Flask.
│   ├── controllers
│   │   └── order_controller.py  # Lógica relacionada con los pedidos.
│   ├── models
│   │   └── order_model.py       # Definición de la estructura de un pedido.
│   ├── routes
│   │   └── order_routes.py      # Configuración de rutas para los pedidos.
│   └── templates
│       ├── home.html           # Plantilla para la página de inicio.
│       └── about.html          # Plantilla para la página "Acerca de".
├── requirements.txt             # Dependencias del proyecto.
└── README.md                    # Documentación del proyecto.
```

## Instalación

1. Clona el repositorio:
   ```
   git clone <URL_DEL_REPOSITORIO>
   cd order-microservice
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Ejecución

Para ejecutar el microservicio, utiliza el siguiente comando:

```
python src/app.py
```

El microservicio estará disponible en `http://localhost:5000`.

## Uso

- **Registrar un pedido**: Envía una solicitud POST a `/orders` con los detalles del pedido.
- **Obtener pedidos**: Envía una solicitud GET a `/orders` para recuperar la lista de pedidos registrados.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.