class ApiError(Exception):
    code = 422
    description = "Default message"

class InvalidData(ApiError):
    code = 400
    description = "Invalid data"
    
class PasswordMismatch(ApiError):
    code = 400
    description = "Password mismatch"

class InvalidName(ApiError):
    code = 400
    description = "Invalid name value, it should have at least 3 characters and maximun 100. Accepts letters, digits, '-', '.' and spaces."

class InvalidCountry(ApiError):
    code = 400
    description = "Invalid country value, it should be an American Country"

class InvalidContact(ApiError):
    code = 400
    description = "Invalid contact value, it should have at least 3 characters and maximun 100. Accepts letters and spaces."

class InvalidTelephone(ApiError):
    code = 400
    description = "Invalid telephone, it should have at least 7 digits and 15 maximum. Digits only."

class InvalidEmail(ApiError):
    code = 400
    description = "Invalid email, it should have email structure."