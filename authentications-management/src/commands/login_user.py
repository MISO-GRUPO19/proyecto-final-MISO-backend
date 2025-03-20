from flask_jwt_extended import create_access_token, create_refresh_token
from ..models.users import Users
from ..errors.errors import UserNotFound, InvalidPassword

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

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role.value if hasattr(user, 'role') else 'user'
            }
        }