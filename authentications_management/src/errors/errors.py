class ApiError(Exception):
    code = 422
    description = "Default message"

class InvalidData(ApiError):
    code = 400
    description = "Datos inválidos"

class PasswordDoesNotHaveTheStructure(ApiError):
    code = 400
    description = "La contraseña no cumple con la estructura requerida"

class EmailDoesNotValid(ApiError):
    code = 400
    description = "Correo electrónico inválido"
    
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
    code = 401 
    description = "Contraseña inválida"


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

class ExistingSeller(ApiError):
    code = 409
    description = "A seller with the same identification already exists in the system"

class InvalidTelephoneCustomer(ApiError):
    code = 400
    description = "InvalidTelephoneCustomer"
    
class InvalidAddressCustomer(ApiError):
    code = 400
    description = "InvalidAddressCustomer"

class InvalidNameCustomer(ApiError):
    code = 400
    description = "InvalidNameValueCustomer"

class SellerNotFound(ApiError):
    code = 404
    description = "SellerNotFound"