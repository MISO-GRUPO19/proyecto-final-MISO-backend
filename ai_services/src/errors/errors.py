class ApiError(Exception):
    code = 422
    description = "Default message"

class InvalidData(ApiError):
    code = 400
    description = "Invalid data"
    
class PasswordMismatch(ApiError):
    code = 400
    description = "Password mismatch"

class InvalidDate(ApiError):
    code = 400
    description = "Invalid Date"