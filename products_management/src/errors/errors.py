class ApiError(Exception):
    code = 422
    description = "Default message"

class InvalidData(ApiError):
    code = 400
    description = "Datos inválidos"
    
class NotFile(ApiError):
    code = 400
    description = "No se ha enviado un archivo"