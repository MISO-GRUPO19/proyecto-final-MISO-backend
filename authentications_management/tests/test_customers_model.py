from authentications_management.src.models.customers import Customers

def test_create_customer_model():
    customer = Customers(
        firstName='John',
        lastName='Doe',
        country='USA',
        address='123 Main St',
        phoneNumber='+12345678901',
        email='john.doe@example.com'
    )
    assert customer.firstName == 'John'
    assert customer.lastName == 'Doe'
    assert customer.email == 'john.doe@example.com'