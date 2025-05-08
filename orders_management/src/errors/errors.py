class ApiError(Exception):
    code = 422
    description = "Default message"

class InvalidData(ApiError):
    code = 400
    description = "Invalid data"
    
class ProductInsufficientStock(ApiError):
    code = 422
    description = "ProductInsufficientStock"
    
class ProductNotFound(ApiError):
    code = 404
    description = "ProductNotFound"