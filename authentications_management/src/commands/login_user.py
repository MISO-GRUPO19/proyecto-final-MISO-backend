from flask_jwt_extended import create_access_token, create_refresh_token
from ..models.users import Users
from ..models.customers import Customers
from ..models.sellers import Sellers
from ..errors.errors import UserNotFound, InvalidPassword
from datetime import timedelta

class LoginUserCommand:
    def __init__(self, email, password):
        self.email = email.strip().lower()
        self.password = password

    def execute(self):
        user = Users.query.filter_by(email=self.email).first()
        if not user:
            raise UserNotFound()

        if not user.check_password(self.password):
            raise InvalidPassword()

        access_token = create_access_token(identity=user.id,expires_delta=timedelta(days=7))
        refresh_token = create_refresh_token(identity=user.id)
        
        if user.role.value == 3:
            isCustomer = False
            customer_id = user.id
            customer = Customers.query.filter_by(email=self.email).first()
            if customer:
                isCustomer = True
                customer_id = customer.id                
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': customer_id,
                    'email': user.email,
                    'role': user.role.value if hasattr(user, 'role') else 'customer'
                },
                'isCustomer': isCustomer
            }

        elif user.role.value == 2:
            isCustomer = False
            seller = Sellers.query.filter_by(email=self.email).first()

            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': seller.id,
                    'email': user.email,
                    'role': user.role.value if hasattr(user, 'role') else 'customer'
                }
            }
        else:
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'role': user.role.value if hasattr(user, 'role') else 'user'
                }
            }