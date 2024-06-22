from model.User import User


class UserService:

    @staticmethod
    def create(user: User):
        user.create()
