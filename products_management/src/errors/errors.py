class ApiError(Exception):
    code = 422
    description = "Default message"

class InvalidData(ApiError):
    code = 400
    description = "Datos inválidos"
    
class NotFile(ApiError):
    code = 400
    description = "No se ha enviado un archivo"

# Mensajes de error específicos
ERROR_MESSAGES = {
    "invalid_name": "El nombre debe tener entre 3 y 100 caracteres y solo puede contener letras, números, '-', '.' y espacios.",
    "invalid_category": "Categoría inválida. Seleccione una de la lista predefinida.",
    "invalid_provider": "Proveedor inválido. Debe ser un UUID válido.",
    "invalid_weight": "Peso inválido.",
    "invalid_weight_less_than_zero": "El peso debe ser mayor que cero.",
    "invalid_price": "Precio inválido. Debe ser un número válido.",
    "invalid_description": "La descripción debe tener entre 3 y 100 caracteres y solo puede contener letras, números, '-', '.' y espacios.",
    "invalid_best_before": "La fecha de vencimiento debe ser mayor o igual a la fecha actual.",
    "invalid_date_format": "Formato de fecha inválido. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS)."
}