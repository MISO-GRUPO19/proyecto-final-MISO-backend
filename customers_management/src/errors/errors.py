class ApiError(Exception):
    code = 422
    description = "Default message"

class InvalidData(ApiError):
    code = 400
    description = "Invalid data"
    
class PasswordMismatch(ApiError):
    code = 400
    description = "Password mismatch"

class CustomerNotFound(ApiError):
    code = 404
    description = 'Customer was not found'