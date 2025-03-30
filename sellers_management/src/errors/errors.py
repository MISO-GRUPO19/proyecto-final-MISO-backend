class ApiError(Exception):
    code = 422
    description = "Default message"

class InvalidData(ApiError):
    code = 400
    description = "Invalid data"

class InvalidIdentification(ApiError):
    code = 400
    description = "Invalid identification value, It should have at least 6 characters and maximum 20, alphanumeric characters only."

class InvalidName(ApiError):
    code = 400
    description = "Invalid name value, It should have at least 3 characters and maximum 100, letters and spaces only."

class InvalidCountry(ApiError):
    code = 400
    description = "Invalid Country, It should be an American country"

class InvalidAddress(ApiError):
    code = 400
    description = "Invalid address, it should have at least 10 characteres and maximum 200."

class InvalidTelephone(ApiError):
    code = 400
    description = "Invalid telephone, it should have at least 7 digits and 15 maximum. Digits only."

class InvalidEmail(ApiError):
    code = 400
    description = "Invalid email, it should have email structure."
