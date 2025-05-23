class ApiError(Exception):
    code = 422
    description = "Default message"

class InvalidData(Exception):
    def __init__(self, errors):
        self.errors = errors
        super().__init__(", ".join(errors))
    
class NotFile(ApiError):
    code = 400
    description = "No se ha enviado un archivo"

class InvalidFileFormat(ApiError):
    code = 400
    description = "Formato de archivo inválido"
    
class ValidationError(ApiError):
    code = 400
    description = "Error de validación"
class NotFound(ApiError):
    code = 404
    description = "No se encontró el producto"

class ProductNotFound(ApiError):
    code = 404
    description = "ProductNotFound"
    
class ProductInsufficientStock(ApiError):
    code = 422
    description = "ProductInsufficientStock"

# Mensajes de error específicos
ERROR_MESSAGES = {
    "invalid_name": "El nombre debe tener entre 3 y 100 caracteres y solo puede contener letras, números, '-', '.' y espacios.",
    "invalid_provider": "Proveedor inválido. Debe ser un UUID válido.",
    "invalid_weight": "Peso inválido. Debe ser un número válido mayor que cero.",
    "invalid_weight_less_than_zero": "El peso debe ser mayor que cero.",
    "invalid_price": "Precio inválido. Debe ser un número válido.",
    "invalid_description": "La descripción debe tener entre 3 y 100 caracteres y solo puede contener letras, números, '-', '.' y espacios.",
    "invalid_best_before": "La fecha de vencimiento debe ser mayor o igual a la fecha actual.",
    "invalid_date_format": "Formato de fecha inválido. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS).",
    "invalid_file_format": "El archivo no tiene el formato esperado.",
    "invalid_product_name": "Nombre del producto inválido.",
    "invalid_weight_price_quantity": "Peso, precio o cantidad no son válidos.",
    "invalid_category": "Categoría inválida",
    "invalid_provider": "Proveedor inválido.",
    "not_found": "El producto no existe"
}