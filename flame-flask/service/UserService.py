from flask_jwt_extended import get_jwt_identity, jwt_required
from model.User import UserIdentity
from model.User import User


class UserService:

    @staticmethod
    def create(user: User):
        user.create()

@jwt_required()
def get_user_indentity() -> UserIdentity:
    identity_dict = get_jwt_identity()
    return UserIdentity(**identity_dict)
