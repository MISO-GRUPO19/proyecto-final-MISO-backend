class ApiError(Exception):
    code = 422
    description = "Default message"

class InvalidData(ApiError):
    code = 400
    description = "Datos inválidos"
    
class PasswordMismatch(ApiError):
    code = 400
    description = "Confirmación de contraseña no coincide"
    
class UserNotFound(ApiError):
    code = 404
    description = "Usuario no encontrado"
    
class UserAlreadyExists(ApiError):
    code = 400
    description = "Usuario ya existe"
    
class Unauthorized(ApiError):
    code = 401
    description = "No autorizado"
    
class InvalidPassword(ApiError):
    code = 400 
    description = "Contraseña inválida"